"""
resource.py
General-purpose resource.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    RESOURCE_INFO_FIELDS,
    GKMAS_VERSION,
    CHARACTER_ABBREVS,
)

import re
from hashlib import md5
from pathlib import Path
from typing import Tuple


logger = Logger()


class GkmasResource:
    """
    A general-purpose binary resource, presumably multimedia instead of an assetbundle.

    Attributes:
        id (int): Resource ID, unique across manifests.
        name (str): Human-readable name, unique across manifests.
        objectName (str): Object name on server, 6-character alphanumeric.
        size (int): Resource size in bytes, used for integrity check.
        md5 (str): MD5 hash of the resource, used for integrity check.
        state (str): Resource state in manifest (ADD/UPDATE), unused for now.
            Other possible states of NONE, LATEST, and DELETE have not yet been observed.
    """

    def __init__(self, info: dict):
        """
        Initializes a resource with the given information.
        Usually called from GkmasManifest.

        Args:
            info (dict): An info dictionary.
                Must contain the following keys: id, name, objectName, size, md5, state.
        """

        for field in RESOURCE_INFO_FIELDS:
            if field != "uploadVersionId":
                setattr(self, field, info[field])
            else:
                setattr(self, field, info.get(field, GKMAS_VERSION))
                # this might be missing in older manifests

        # 'self.state' unused, but retained for compatibility
        self._idname = f"RS[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<GkmasResource {self._idname}>"

    def _get_canon_repr(self):
        # this format retains the order of fields
        return {field: getattr(self, field) for field in RESOURCE_INFO_FIELDS}

    # No leading underscore, since this should be client-side visible
    def get_caption(self) -> str:
        raise NotImplementedError
