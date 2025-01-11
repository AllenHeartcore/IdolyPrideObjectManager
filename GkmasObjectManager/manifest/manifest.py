"""
manifest.py
Manifest decryption, exporting, and object downloading.
"""

from ..object import GkmasAssetBundle, GkmasResource
from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    ALL_ASSETBUNDLES,
    ALL_RESOURCES,
    IMG_RESIZE_ARGTYPE,
    DEFAULT_DOWNLOAD_PATH,
    DEFAULT_DOWNLOAD_NWORKER,
    DICLIST_IGNORED_FIELDS,
    CSV_COLUMNS,
)

from .octodb_pb2 import dict2pdbytes
from .utils import Diclist, ConcurrentDownloader

import re
import json
import pandas as pd
from pathlib import Path


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

    # ------------ EXPORT ------------ #

    def export(self, path: PATH_ARGTYPE):
        """
        Exports the manifest as ProtoDB, JSON, and/or CSV to the specified path.
        This is a dispatcher method.

        Args:
            path (Union[str, Path]): A directory or a file path.
                If a directory, all three formats are exported.
                If a file path, the format is determined by the extension
                (all extensions other than .json and .csv are treated as raw binary
                and therefore exported as ProtoDB).
        """

        path = Path(path)

        if path.suffix == "":
            # used to be path.is_dir(), but it also returns False for non-existent dirs
            path.mkdir(parents=True, exist_ok=True)
            self._export_pdb(path / f"manifest_v{self.revision}.pdb")
            self._export_json(path / f"manifest_v{self.revision}.json")
            self._export_csv(path / f"manifest_v{self.revision}.csv")

        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".pdb":
                self._export_pdb(path)
            elif path.suffix == ".json":
                self._export_json(path)
            elif path.suffix == ".csv":
                self._export_csv(path)
            else:
                logger.warning("Unrecognized file extension, abort")

    def _export_pdb(self, path: Path):
        """
        [INTERNAL] Writes raw protobuf bytes into the specified path.
        """
        try:
            path.write_bytes(dict2pdbytes(self.jdict))
            logger.success(f"ProtoDB has been written into {path}")
        except:
            logger.warning(f"Failed to write ProtoDB into {path}")

    def _export_json(self, path: Path):
        """
        [INTERNAL] Writes JSON-serialized dictionary into the specified path.
        """
        try:
            path.write_text(json.dumps(self.jdict, indent=4))
            logger.success(f"JSON has been written into {path}")
        except:
            logger.warning(f"Failed to write JSON into {path}")

    def _export_csv(self, path: Path):
        """
        [INTERNAL] Writes CSV-serialized data into the specified path.
        Assetbundles and resources are concatenated into a single table and sorted by name.
        Assetbundles can be distinguished by their '.unity3d' suffix.
        """
        dfa = pd.DataFrame(self._abl, columns=CSV_COLUMNS)
        dfa["name"] = dfa["name"].apply(lambda x: x + ".unity3d")
        dfr = pd.DataFrame(self._resl, columns=CSV_COLUMNS)
        df = pd.concat([dfa, dfr], ignore_index=True)
        df.sort_values("name", inplace=True)
        try:
            df.to_csv(path, index=False)
            logger.success(f"CSV has been written into {path}")
        except:
            logger.warning(f"Failed to write CSV into {path}")

    # ----------- DOWNLOAD ----------- #

    def download(
        self,
        *criteria: str,
        nworker: int = DEFAULT_DOWNLOAD_NWORKER,
        path: PATH_ARGTYPE = DEFAULT_DOWNLOAD_PATH,
        categorize: bool = True,
        extract_img: bool = True,
        img_format: str = "png",
        img_resize: IMG_RESIZE_ARGTYPE = None,
    ):
        """
        Downloads the regex-specified assetbundles/resources to the specified path.

        Args:
            *criteria (str): Regex patterns of assetbundle/resource names.
                Allowed special tokens are const.ALL_ASSETBUNDLES and const.ALL_RESOURCES.
            nworker (int) = DEFAULT_DOWNLOAD_NWORKER: Number of concurrent download workers.
                Defaults to multiprocessing.cpu_count().
            path (Union[str, Path]) = DEFAULT_DOWNLOAD_PATH: A directory to which the objects are downloaded.
                *WARNING: Behavior is undefined if the path points to an definite file (with extension).*
            categorize (bool) = True: Whether to categorize the downloaded objects into subdirectories.
                If False, all objects are downloaded to the specified 'path' in a flat structure.
            extract_img (bool) = True: Whether to extract images from assetbundles of type 'img'.
                If False, 'img_.*\\.unity3d' are downloaded as is.
            img_format (str) = 'png': Image format for extraction. Case-insensitive.
                Effective only when 'extract_img' is True. Format must support RGBA mode.
                Valid options are checked by PIL.Image.save() and are not enumerated.
            img_resize (Union[None, str, Tuple[int, int]]) = None: Image resizing argument.
                If None, images are downloaded as is.
                If str, string must contain exactly one ':' and images are resized to the specified ratio.
                If Tuple[int, int], images are resized to the specified exact dimensions.
        """

        objects = []

        for criterion in criteria:
            if criterion == ALL_ASSETBUNDLES:  # special tokens, enclosed in <>
                objects.extend(self.abs)
            elif criterion == ALL_RESOURCES:
                objects.extend(self.reses)
            else:
                objects.extend(
                    [
                        self._name2object[file]
                        for file in self._name2object
                        if re.match(criterion, file)
                    ]
                )

        ConcurrentDownloader(nworker).dispatch(
            objects,
            path=path,
            categorize=categorize,
            extract_img=extract_img,
            img_format=img_format,
            img_resize=img_resize,
        )
