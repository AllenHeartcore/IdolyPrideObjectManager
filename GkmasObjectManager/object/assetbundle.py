"""
assetbundle.py
Asset bundle handling.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    RESOURCE_INFO_FIELDS_HEAD,
    RESOURCE_INFO_FIELDS_TAIL,
)

from .resource import GkmasResource

from pathlib import Path


logger = Logger()


class GkmasAssetBundle(GkmasResource):
    """
    An assetbundle. Class inherits from GkmasResource.
    """

    def __init__(self, info: dict):
        """
        Initializes an assetbundle with the given information.
        Usually called from GkmasManifest.

        Args:
            info (dict): An info dictionary.
                Must contain the following keys: id, name, objectName, size, md5.
        """

        super().__init__(info)
        self.dependencies = info.get("dependencies", [])
        self._idname = f"AB[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<GkmasAssetBundle {self._idname}>"

    def _get_canon_repr(self):
        ret = {field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_HEAD}
        if self.dependencies:
            ret["dependencies"] = self.dependencies  # for ordering
        ret.update({field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_TAIL})
        return ret
