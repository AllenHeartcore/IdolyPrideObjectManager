"""
utils.py
List operation and concurrent downloading utilities.
"""

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    def __init__(self, diclist: list):
        super().__init__(diclist.copy())
        # such that all subsequent operations (especially rip_field)
        # are non-destructive to the original list

    def __sub__(self, other: "Diclist") -> "Diclist":
        return Diclist([item for item in self if item not in other])

    def rip_field(self, targets: list) -> "Diclist":
        return Diclist(
            [{k: v for k, v in entry.items() if k not in targets} for entry in self]
        )

    def diff(self, other: "Diclist", ignored_fields: list = []) -> "Diclist":

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
