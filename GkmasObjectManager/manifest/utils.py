"""
utils.py
List operation and concurrent downloading utilities.
"""

from ..const import (
    DICLIST_INDEX_FIELD,
    DICLIST_NAME_FIELD,
    DICLIST_DIFF_IGNORED_FIELDS,
)

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union


class Diclist(list):
    """
    A list of dictionaries, optimized for comparison.

    Methods:
        __sub__(other: Diclist) -> Diclist:
            Subtracts another Diclist from this Diclist.
            Returns the list of elements unique to 'self'.
        rip_field(targets: list) -> Diclist:
            Removes selected fields from all dictionaries.
        diff(other: Diclist, ignored_fields: list) -> Diclist:
            Compares two Diclists while ignoring selected fields,
            but **retains all fields** in the reconstructed output.
    """

    def __init__(self, diclist: list, sort_by: str = DICLIST_INDEX_FIELD):

        diclist = diclist.copy()
        # such that all subsequent operations (especially rip_field)
        # are non-destructive to the original list

        if sort_by:
            diclist.sort(key=lambda x: x[sort_by])

        super().__init__(diclist)

    def __getitem__(self, key: Union[int, str]) -> dict:
        for item in self:
            if (isinstance(key, int) and item[DICLIST_INDEX_FIELD] == key) or (
                isinstance(key, str) and item[DICLIST_NAME_FIELD] == key
            ):
                return item
        raise KeyError

    def __sub__(self, other: "Diclist") -> "Diclist":
        return Diclist([item for item in self if item not in other])

    def rip_field(self, targets: list) -> "Diclist":
        return Diclist(
            [{k: v for k, v in entry.items() if k not in targets} for entry in self]
        )

    def diff(
        self, other: "Diclist", ignored_fields: list = DICLIST_DIFF_IGNORED_FIELDS
    ) -> "Diclist":

        if not ignored_fields:
            return self - other

        # rip unused fields for comparison
        self_rip = self.rip_field(ignored_fields)
        other_rip = other.rip_field(ignored_fields)

        # retain complete fields for output
        return Diclist([self[self_rip.index(entry)] for entry in self_rip - other_rip])


class ConcurrentDownloader:
    """
    A multithreaded downloader for objects on server.

    Methods:
        dispatch(objects: list, **kwargs):
            Downloads a list of objects to a specified path.
            Executor implicitly calls object.GkmasResource.download() with **kwargs.
    """

    def __init__(self, nworker: int):
        self.nworker = nworker

    def dispatch(self, objects: list, **kwargs):
        # don't use *args here to avoid fixed order

        # not initialized in __init__ to avoid memory leak
        self.executor = ThreadPoolExecutor(max_workers=self.nworker)

        futures = [self.executor.submit(obj.download, **kwargs) for obj in objects]
        for future in as_completed(futures):
            future.result()

        self.executor.shutdown()
