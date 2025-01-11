"""
manifest.py
Manifest decryption, exporting, and object downloading.
"""

from ..object import GkmasAssetBundle, GkmasResource
from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    IMG_RESIZE_ARGTYPE,
    ALL_ASSETBUNDLES,
    ALL_RESOURCES,
    CSV_COLUMNS,
    DEFAULT_DOWNLOAD_PATH,
    DEFAULT_DOWNLOAD_NWORKER,
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
        assetbundles (Diclist): List of assetbundle *info dictionaries*.
        resources (Diclist): List of resource *info dictionaries*.
    *Documentation for Diclist can be found in utils.py.*

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
        """
        self.revision = jdict["revision"]
        self.assetbundles = Diclist(jdict["assetBundleList"])
        self.resources = Diclist(jdict["resourceList"])
        # 'jdict' is then discarded and losslessly reconstructed at export

    def __repr__(self):
        return f"<GkmasManifest revision {self.revision} with {len(self.assetbundles)} assetbundles and {len(self.resources)} resources>"

    def __getitem__(self, key: str):
        try:
            return GkmasAssetBundle(self.assetbundles[key])
        except KeyError:
            return GkmasResource(self.resources[key])

    def __iter__(self):
        for ab in self.assetbundles:
            yield GkmasAssetBundle(ab)
        for res in self.resources:
            yield GkmasResource(res)

    def __len__(self):
        return len(self.assetbundles) + len(self.resources)

    def __contains__(self, key: str):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __sub__(self, other):
        """
        [INTERNAL] Creates a manifest from a differentiation dictionary.
        The diffdict refers to a dictionary containing differentiated
        assetbundles and resources, created by utils.Diclist.diff().
        """
        return GkmasManifest(
            {
                "revision": f"{self.revision}-{other.revision}",
                "assetBundleList": self.assetbundles.diff(other.assetbundles),
                "resourceList": self.resources.diff(other.resources),
            }
        )

    def _get_jdict(self):
        """
        [INTERNAL] Returns the JSON dictionary of the manifest.
        """
        return {
            "revision": self.revision,
            "assetBundleList": self.assetbundles,
            "resourceList": self.resources,
        }

    # ------------ EXPORT ------------ #

    def export(self, path: PATH_ARGTYPE, format: str = "infer"):
        """
        Exports the manifest as ProtoDB, JSON, and/or CSV to the specified path.
        This is a dispatcher method.

        Args:
            path (Union[str, Path]): A file path.
                The format is determined by the extension if 'format' is 'infer'.
                (All extensions other than .json and .csv are inferred
                as raw binary and therefore exported as ProtoDB, but
                a warning is issued if the extension is not .pdb.)
            format (str) = 'infer': The format to export.
                Should be one of 'pdb', 'json', 'csv', or 'infer'.
        """

        path = Path(path)

        if format == "infer":
            if path.suffix == ".pdb":
                format = "pdb"
            elif path.suffix == ".json":
                format = "json"
            elif path.suffix == ".csv":
                format = "csv"
            else:
                logger.warning("Unrecognized file extension, defaulting to ProtoDB")
                format = "pdb"

        if format == "pdb":
            self._export_pdb(path)
        elif format == "json":
            self._export_json(path)
        elif format == "csv":
            self._export_csv(path)
        else:
            logger.warning(f"Unrecognized format '{format}', aborted")
            # Could also be logger.error, but let's fail gracefully.
            # This check used to appear in the type hint, but then
            # this method would *silently* fail if the format was invalid.

    def _export_pdb(self, path: Path):
        """
        [INTERNAL] Writes raw protobuf bytes into the specified path.
        """
        try:
            path.write_bytes(dict2pdbytes(self._get_jdict()))
            logger.success(f"ProtoDB has been written into {path}")
        except:
            logger.warning(f"Failed to write ProtoDB into {path}")

    def _export_json(self, path: Path):
        """
        [INTERNAL] Writes JSON-serialized dictionary into the specified path.
        """
        try:
            path.write_text(json.dumps(self._get_jdict(), indent=4))
            logger.success(f"JSON has been written into {path}")
        except:
            logger.warning(f"Failed to write JSON into {path}")

    def _export_csv(self, path: Path):
        """
        [INTERNAL] Writes CSV-serialized data into the specified path.
        Assetbundles and resources are concatenated into a single table and sorted by name.
        Assetbundles can be distinguished by their '.unity3d' suffix.
        """

        # Forced list conversion is necessary since Diclist overrides __iter__,
        # which handles integer keys (index by ID) and messes up with standard modules
        # like pandas that rely on self[0] as a "sample" object from the list.
        dfa = pd.DataFrame(list(self.assetbundles), columns=CSV_COLUMNS)
        dfa["name"] = dfa["name"].apply(lambda x: x + ".unity3d")
        dfr = pd.DataFrame(list(self.resources), columns=CSV_COLUMNS)
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
                objects.extend([])

        ConcurrentDownloader(nworker).dispatch(
            objects,
            path=path,
            categorize=categorize,
            extract_img=extract_img,
            img_format=img_format,
            img_resize=img_resize,
        )
