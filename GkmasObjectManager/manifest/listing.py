"""
listing.py
"Object list" class holding a list of dictionaries,
optimized for indexing and comparison.
"""

from ..const import (
    OBJLIST_ID_FIELD,
    OBJLIST_NAME_FIELD,
    RESOURCE_INFO_CUSTOM_FIELDS,
)

import requests
from hashlib import md5
from typing import Union


class GkmasObjectList:
    """
    A list of resource metadata, optimized for indexing and comparison.
    Implemented as listing utility wrappers around a list of dictionaries.

    Methods:
        __sub__(other: GkmasObjectList) -> GkmasObjectList:
            Subtracts another object list from this one.
            Returns the list of elements unique to 'self'.
        rip_field(targets: list) -> GkmasObjectList:
            Removes selected fields from all dictionaries.
        diff(other: GkmasObjectList, ignored_fields: list) -> GkmasObjectList:
            Compares two object lists while ignoring selected fields,
            but **retains all fields** in the reconstructed output.
    """

    def __init__(self, infos: list, base_class: object):
        infos.sort(key=lambda x: x[OBJLIST_ID_FIELD])
        self.infos = infos
        self.base_class = base_class
        self._objects = [None] * len(infos)
        self._id_idx = {info[OBJLIST_ID_FIELD]: i for i, info in enumerate(infos)}
        self._name_idx = {info[OBJLIST_NAME_FIELD]: i for i, info in enumerate(infos)}
        # 'self._*_idx' are int/str -> int lookup tables

    def __repr__(self):
        return f"<GkmasObjectList of {len(self.infos)} {self.base_class.__name__}'s>"

    def __getitem__(self, key: Union[int, str]) -> object:

        if isinstance(key, int):
            idx = self._id_idx[key]
        elif isinstance(key, str):
            idx = self._name_idx[key]
        else:
            raise TypeError  # just in case, should never reach here

        if self._objects[idx] is None:
            self._objects[idx] = self.base_class(self.infos[idx])

        return self._objects[idx]

    def __iter__(self):
        for info in self.infos:
            yield self.base_class(info)

    def __len__(self):
        return len(self.infos)

    def __contains__(self, key: str) -> bool:
        return key in self._name_idx
        # 'if <numerical ID> in self' is nonsensical

    def __sub__(self, other: "GkmasObjectList") -> "GkmasObjectList":
        assert self.base_class == other.base_class
        canon_reprs = []
        for entry in self:
            try:
                this_repr = entry._get_canon_repr()
                other_repr = other[entry.name]._get_canon_repr()
            except KeyError:
                canon_reprs.append(this_repr)
                continue
            else:
                if this_repr != other_repr:
                    canon_reprs.append(this_repr)
        return GkmasObjectList(canon_reprs, self.base_class)

    def _get_canon_repr(self):
        """
        [INTERNAL] Returns the JSON-compatible "canonical" representation of the object list.
        """
        return [entry._get_canon_repr() for entry in self]

    def _get_largest_id(self):
        """
        Returns the largest ID in the list.
        A precondition for adding new objects.
        """
        return max(self._id_idx.keys())
        # We don't implement deletion, so we could technically use len(self) - 1,
        # but this is more robust and extensible.

    def _url_to_size_and_md5(self, url: str) -> tuple:
        """
        Returns the size and MD5 hash of the object at the given URL.
        A helper function for add() and edit().
        """
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            raise ValueError(f"Failed to get size and MD5 for {url}")
        return len(response.content), md5(response.content).hexdigest()

    def update(self, id: int, info: dict):
        """
        Adds or edits an object in the list.
        """
        assert set(info.keys()) == set(RESOURCE_INFO_CUSTOM_FIELDS)
        size, md5 = self._url_to_size_and_md5(info["url"])
        info["size"] = size
        info["md5"] = md5

        try:  # edit case
            self.infos[self._id_idx[id]].update(info)
            self._objects[self._id_idx[id]] = None
        except KeyError:  # add case
            self.infos.append(info)
            self._id_idx[id] = len(self.infos) - 1
            self._name_idx[info["name"]] = len(self.infos) - 1
            self._objects.append(None)
