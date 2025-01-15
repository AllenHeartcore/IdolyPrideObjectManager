"""
listing.py
"Object list" class holding a list of dictionaries,
optimized for indexing and comparison.
"""

from ..const import (
    DICLIST_INDEX_FIELD,
    DICLIST_NAME_FIELD,
    DICLIST_DIFF_IGNORED_FIELDS,
)

from typing import Union


class GkmasObjectList:
    """
    A list of dictionaries, optimized for comparison.

    Methods:
        __sub__(other: GkmasObjectList) -> GkmasObjectList:
            Subtracts another GkmasObjectList from this one.
            Returns the list of elements unique to 'self'.
        rip_field(targets: list) -> GkmasObjectList:
            Removes selected fields from all dictionaries.
        diff(other: GkmasObjectList, ignored_fields: list) -> GkmasObjectList:
            Compares two Diclists while ignoring selected fields,
            but **retains all fields** in the reconstructed output.
    """

    def __init__(self, diclist: list, sort_by: str = DICLIST_INDEX_FIELD):

        diclist = diclist.copy()
        # such that all subsequent operations (especially rip_field)
        # are non-destructive to the original list

        if sort_by:
            diclist.sort(key=lambda x: x[sort_by])

    def __getitem__(self, key: Union[int, str]) -> dict:
        for item in self:
            if (isinstance(key, int) and item[DICLIST_INDEX_FIELD] == key) or (
                isinstance(key, str) and item[DICLIST_NAME_FIELD] == key
            ):
                return item
        raise KeyError

    def __sub__(self, other: "GkmasObjectList") -> "GkmasObjectList":
        return GkmasObjectList([item for item in self if item not in other])

    def rip_field(self, targets: list) -> "GkmasObjectList":
        return GkmasObjectList(
            [{k: v for k, v in entry.items() if k not in targets} for entry in self]
        )

    def diff(
        self,
        other: "GkmasObjectList",
        ignored_fields: list = DICLIST_DIFF_IGNORED_FIELDS,
    ) -> "GkmasObjectList":

        if not ignored_fields:
            return self - other

        # rip unused fields for comparison
        self_rip = self.rip_field(ignored_fields)
        other_rip = other.rip_field(ignored_fields)

        # retain complete fields for output
        return GkmasObjectList(
            [self[self_rip.index(entry)] for entry in self_rip - other_rip]
        )
