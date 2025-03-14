"""
manifest.py
Manifest exporting.
"""

from ..object import GkmasResource
from ..log import Logger
from ..const import PATH_ARGTYPE

from .revision import GkmasManifestRevision
from .listing import GkmasObjectList

import re
import json
from pathlib import Path


# The logger would better be a global variable in the
# modular __init__.py, but Python won't allow me to
logger = Logger()


class GkmasManifest:
    """
    A GKMAS manifest, containing info about resources.

    Attributes:
        revision (GkmasManifestRevision): Manifest revision this-diff-base (see revision.py).
        resources (GkmasObjectList): List of resource *info dictionaries*.
    *Documentation for GkmasObjectList can be found in listing.py.*

    Methods:
        export(path: Union[str, Path]) -> None:
            Exports the manifest as JSON to the specified path.
    """

    def __init__(self, jdict: dict, base_revision: int = 0):
        """
        [INTERNAL] Initializes a manifest from the given JSON dictionary.

        Args:
            jdict (dict): JSON-serialized dictionary.
                Must contain 'revision' and 'resourceList' keys.
            base_revision (int) = 0: The revision number of the base manifest.
                Manually specified when loading a diff, at which case
                a warning of conflict is raised if jdict['revision'] is already a tuple.
        """

        revision = jdict["revision"]  # not jdict.get() to enforce presence
        if isinstance(revision, int):
            revision = (revision, 0)
        if base_revision != 0:  # leave negative base handling to the Revision class
            if base_revision != revision[1] != 0:  # equivalent to a 2-AND
                logger.warning(
                    f"Overriding detected base revision v{revision[1]} with specified revision v{base_revision}."
                )
            revision = (revision[0], base_revision)  # proceed anyway

        try:  # instantiate from JSON
            self.revision = GkmasManifestRevision(*revision)
            self.resources = GkmasObjectList(
                jdict.get("resourceList", []),  # might be empty in recent diffs
                GkmasResource,
            )
        except TypeError:  # instantiate from diff, skip type conversion
            self.revision = jdict["revision"]  # won't be missing since ...
            self.resources = jdict["resourceList"]  # this is constructed internally

        # 'jdict' is then discarded and losslessly reconstructed at export

    def __repr__(self):
        return f"<GkmasManifest revision {self.revision} with {len(self.resources)} resources>"

    def __getitem__(self, key: str):
        return self.resources[key]

    def __iter__(self):
        for res in self.resources:
            yield res

    def __len__(self):
        return len(self.resources)

    def __contains__(self, key: str):
        return key in self.resources
        # could also try self[key]

    def __sub__(self, other):
        """
        [INTERNAL] Creates a manifest from a differentiation dictionary.
        The diffdict refers to a dictionary containing differentiated
        resources, created by listing.GkmasObjectList.diff().
        """
        return GkmasManifest(
            {  # this is not a standard JSON dict, more like named arguments
                "revision": self.revision - other.revision,  # handles sanity check
                "resourceList": self.resources - other.resources,
            }
        )

    def _get_canon_repr(self):
        """
        [INTERNAL] Returns the JSON-compatible "canonical" representation of the manifest.
        """
        return {
            "revision": self.revision._get_canon_repr(),
            "resourceList": self.resources._get_canon_repr(),
        }

    def _get_largest_id(self):
        """
        [INTERNAL] Returns the largest ID in the manifest.
        Used by frontend when previewing an add.
        """
        return self.resources._get_largest_id()

    def add(self, info: dict):
        """
        Adds a new resource to the manifest. Handled by listing backend.

        Args:
            info (dict): Dictionary containing resource info.
                Fields must be exactly ["name", "url", "cover", "keywords", "caption"].
        """
        self.resources.add(info)

    def edit(self, id: int, info: dict):
        """
        Edits an existing resource in the manifest. Handled by listing backend.

        Args:
            id (int): ID of the resource to edit.
            info (dict): Dictionary containing resource info.
                Fields must be exactly ["name", "url", "cover", "keywords", "caption"].
        """
        self.resources.edit(id, info)

    def export(self, path: PATH_ARGTYPE):
        """
        Writes JSON-serialized dictionary into the specified path.
        """

        path = Path(path)

        if path.suffix != ".json":
            logger.warning("Attempting to write JSON into a non-.json file")

        try:
            path.write_text(
                json.dumps(self._get_canon_repr(), indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.success(f"JSON has been written into {path}")
        except:
            logger.error(f"Failed to write JSON into {path}")

    def search(self, criterion: str):
        """
        Searches the manifest for objects matching the specified criterion.
        Returns a list of object names.

        Args:
            criterion (str): Regex pattern of object names.
        """

        names = []
        for obj in self:
            if re.match(criterion, obj.name, flags=re.IGNORECASE):
                names.append(obj.name)
        return [self[name] for name in sorted(names)]
        # This will be called by frontend.
        # We instantiate here to make ID's readily available.
