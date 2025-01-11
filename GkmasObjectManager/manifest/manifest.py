"""
manifest.py
Manifest decryption, exporting, and object downloading.
"""

from ..log import Logger
from ..const import PATH_ARGTYPE, DICLIST_IGNORED_FIELDS


from .utils import Diclist
from ..const import (
    PATH_ARGTYPE,
    GKMAS_API_URL,
    GKMAS_API_HEADER,
    GKMAS_ONLINEPDB_KEY,
    GKMAS_OCTOCACHE_KEY,
    GKMAS_OCTOCACHE_IV,
)

from .decrypt import AESCBCDecryptor
from ..object import GkmasAssetBundle, GkmasResource

import requests
from pathlib import Path
from urllib.parse import urljoin
from google.protobuf.json_format import MessageToDict


# The logger would better be a global variable in the
# modular __init__.py, but Python won't allow me to
logger = Logger()


class GkmasManifest:
    """
    A GKMAS manifest, containing info about assetbundles and resources.

    Attributes:
        revision (str): Manifest revision, a number or a string (for manifest from diff).
        jdict (dict): JSON-serialized dictionary of the protobuf.
        abs (list): List of GkmasAssetBundle objects.
        reses (list): List of GkmasResource objects.

    Methods:
        download(
            *criteria: str,
            nworker: int = DEFAULT_DOWNLOAD_NWORKER,
            path: Union[str, Path] = DEFAULT_DOWNLOAD_PATH,
            categorize: bool = True,
            extract_img: bool = True,
            img_format: str = "png",
            img_resize: Union[None, str, Tuple[int, int]] = None,
        ) -> None:
            Downloads the regex-specified assetbundles/resources to the specified path.
        export(path: Union[str, Path]) -> None:
            Exports the manifest as ProtoDB, JSON, and/or CSV to the specified path.
    """

    # It's necessary to import all methods instead of merely interface/dispatcher functions;
    # otherwise, self._helper_method() in these interface functions would encounter name
    # resolution errors. Also, import * is prohibited unless importing from a module.
    from ._download import download
    from ._export import export, _export_pdb, _export_json, _export_csv

    def __init__(self, jdict: dict):
        """
        [INTERNAL] Initializes a manifest from the given JSON dictionary.

        Args:
            jdict (dict): JSON-serialized dictionary extracted from protobuf.
                Must contain 'revision', 'assetBundleList', and 'resourceList' keys.

        Internal attributes:
            _abl (Diclist): List of assetbundle *info dictionaries*.
            _resl (Diclist): List of resource *info dictionaries*.
            _name2object (dict): Mapping from object name to GkmasAssetBundle/GkmasResource.

        Documentation for Diclist can be found in utils.py.
        """
        jdict["assetBundleList"] = sorted(
            jdict["assetBundleList"], key=lambda x: x["id"]
        )
        jdict["resourceList"] = sorted(jdict["resourceList"], key=lambda x: x["id"])
        self.jdict = jdict
        self.revision = jdict["revision"]
        self._abl = Diclist(self.jdict["assetBundleList"])
        self._resl = Diclist(self.jdict["resourceList"])
        self.abs = [GkmasAssetBundle(ab) for ab in self._abl]
        self.reses = [GkmasResource(res) for res in self._resl]
        self._name2object = {ab.name: ab for ab in self.abs}  # quick lookup
        self._name2object.update({res.name: res for res in self.reses})
        logger.info(f"Found {len(self.abs)} assetbundles")
        logger.info(f"Found {len(self.reses)} resources")
        logger.info(f"Detected revision: {self.revision}")

    def __repr__(self):
        return f"<GkmasManifest revision {self.revision}>"

    def __getitem__(self, key: str):
        return self._name2object[key]

    def __iter__(self):
        return iter(self._name2object.values())

    def __len__(self):
        return len(self._name2object)

    def __contains__(self, key: str):
        return key in self._name2object

    def __sub__(self, other):
        """
        [INTERNAL] Creates a manifest from a differentiation dictionary.
        The diffdict refers to a dictionary containing differentiated
        assetbundles and resources, created by utils.Diclist.diff().
        """
        manifest = GkmasManifest()
        manifest.revision = f"{self.revision}-{other.revision}"
        manifest._parse_jdict(
            {
                "assetBundleList": self._abl.diff(other._abl, DICLIST_IGNORED_FIELDS),
                "resourceList": self._resl.diff(other._resl, DICLIST_IGNORED_FIELDS),
            }
        )
        logger.info("Manifest created from differentiation")
        return manifest
