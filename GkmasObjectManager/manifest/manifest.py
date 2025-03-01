"""
manifest.py
Manifest decryption, exporting, and object downloading.
"""

from ..object import GkmasAssetBundle, GkmasResource
from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    CSV_COLUMNS,
    DEFAULT_DOWNLOAD_PATH,
    DEFAULT_DOWNLOAD_NWORKER,
)

from .revision import GkmasManifestRevision
from .octodb_pb2 import dict2pdbytes
from .listing import GkmasObjectList

import re
import json
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# The logger would better be a global variable in the
# modular __init__.py, but Python won't allow me to
logger = Logger()


class GkmasManifest:
    """
    A GKMAS manifest, containing info about assetbundles and resources.

    Attributes:
        revision (GkmasManifestRevision): Manifest revision this-diff-base (see revision.py).
        assetbundles (GkmasObjectList): List of assetbundle *info dictionaries*.
        resources (GkmasObjectList): List of resource *info dictionaries*.
        urlformat (str): URL format for downloading assetbundles/resources.
            Solely for faithful reconstruction of the manifest.
    *Documentation for GkmasObjectList can be found in listing.py.*

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

    def __init__(self, jdict: dict, base_revision: int = 0):
        """
        [INTERNAL] Initializes a manifest from the given JSON dictionary.

        Args:
            jdict (dict): JSON-serialized dictionary extracted from protobuf.
                Must contain 'revision', 'assetBundleList', 'resourceList',
                and 'urlFormat' keys.
            base_revision (int) = 0: The revision number of the base manifest.
                Manually specified when loading a diff, at which case
                a warning of conflict is raised if jdict['revision'] is already a tuple.
        """

        revision = jdict["revision"]  # not jdict.get() to enforce presence; same below
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
            self.assetbundles = GkmasObjectList(
                jdict["assetBundleList"],
                GkmasAssetBundle,
            )
            self.resources = GkmasObjectList(
                jdict["resourceList"],
                GkmasResource,
            )
        except TypeError:  # instantiate from diff, skip type conversion
            self.revision = jdict["revision"]
            self.assetbundles = jdict["assetBundleList"]
            self.resources = jdict["resourceList"]

        self.urlformat = jdict["urlFormat"]
        # 'jdict' is then discarded and losslessly reconstructed at export

    def __repr__(self):
        return f"<GkmasManifest revision {self.revision} with {len(self.assetbundles)} assetbundles and {len(self.resources)} resources>"

    def __getitem__(self, key: str):
        try:
            return self.assetbundles[key]
        except KeyError:
            return self.resources[key]
            # any more KeyError's are raised as is

    def __iter__(self):
        for ab in self.assetbundles:
            yield ab
        for res in self.resources:
            yield res

    def __len__(self):
        return len(self.assetbundles) + len(self.resources)

    def __contains__(self, key: str):
        return key in self.assetbundles or key in self.resources
        # could also try self[key]

    def __sub__(self, other):
        """
        [INTERNAL] Creates a manifest from a differentiation dictionary.
        The diffdict refers to a dictionary containing differentiated
        assetbundles and resources, created by listing.GkmasObjectList.diff().
        """
        return GkmasManifest(
            {  # this is not a standard JSON dict, more like named arguments
                "revision": self.revision - other.revision,  # handles sanity check
                "assetBundleList": self.assetbundles - other.assetbundles,
                "resourceList": self.resources - other.resources,
                "urlFormat": self.urlformat,
                # always override with the higher revision, in case this ever differs
            }
        )

    def _get_canon_repr(self):
        """
        [INTERNAL] Returns the JSON-compatible "canonical" representation of the manifest.
        """
        return {
            "revision": self.revision._get_canon_repr(),
            "assetBundleList": self.assetbundles._get_canon_repr(),
            "resourceList": self.resources._get_canon_repr(),
            "urlFormat": self.urlformat,
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

        if path.suffix != ".pdb":
            logger.warning("Attempting to write ProtoDB into a non-.pdb file")

        jdict = self._get_canon_repr()
        if isinstance(jdict["revision"], tuple):
            logger.warning("Exporting a diff manifest as ProtoDB, base revision lost")
            jdict["revision"] = jdict["revision"][0]

        try:
            path.write_bytes(dict2pdbytes(jdict))
            logger.success(f"ProtoDB has been written into {path}")
        except:
            logger.error(f"Failed to write ProtoDB into {path}")

    def _export_json(self, path: Path):
        """
        [INTERNAL] Writes JSON-serialized dictionary into the specified path.
        """

        if path.suffix != ".json":
            logger.warning("Attempting to write JSON into a non-.json file")

        try:
            path.write_text(json.dumps(self._get_canon_repr(), indent=4))
            logger.success(f"JSON has been written into {path}")
        except:
            logger.error(f"Failed to write JSON into {path}")

    def _export_csv(self, path: Path):
        """
        [INTERNAL] Writes CSV-serialized data into the specified path.
        Assetbundles and resources are concatenated into a single table and sorted by name.
        Assetbundles can be distinguished by their '.unity3d' suffix.
        """

        if path.suffix != ".csv":
            logger.warning("Attempting to write CSV into a non-.csv file")

        # [RESOLVED] Forced list conversion is necessary since GkmasObjectList overrides __iter__,
        # which handles integer keys (index by ID) and messes up with standard modules
        # like pandas that rely on self[0] as a "sample" object from the list.
        dfa = pd.DataFrame(self.assetbundles._get_canon_repr(), columns=CSV_COLUMNS)
        dfa["name"] = dfa["name"].apply(lambda x: x + ".unity3d")
        dfr = pd.DataFrame(self.resources._get_canon_repr(), columns=CSV_COLUMNS)
        df = pd.concat([dfa, dfr], ignore_index=True)
        df.sort_values("name", inplace=True)

        try:
            df.to_csv(path, index=False)
            logger.success(f"CSV has been written into {path}")
        except:
            logger.error(f"Failed to write CSV into {path}")

    # ----------- DOWNLOAD ----------- #

    def search(self, criterion: str):
        """
        Searches the manifest for objects matching the specified criterion.
        Returns a list of object names.

        Args:
            criterion (str): Regex pattern of object names.
        """

        names = []
        for obj in self:
            if re.match(criterion, obj.name):
                names.append(obj.name)
        return [self[name] for name in sorted(names)]
        # This will be called by frontend.
        # We instantiate here to make ID's readily available.

    def download(
        self,
        *criteria: str,
        nworker: int = DEFAULT_DOWNLOAD_NWORKER,
        **kwargs,
    ):
        """
        Downloads the regex-specified assetbundles/resources to the specified path.

        Args:
            *criteria (str): Regex patterns of assetbundle/resource names.
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
            objects.extend(self.search(criterion))

        if not objects:
            logger.warning("No objects matched the criteria, aborted")
            return

        self._do_download(objects, nworker, **kwargs)

    def download_all_assetbundles(
        self, nworker: int = DEFAULT_DOWNLOAD_NWORKER, **kwargs
    ):
        """
        Downloads all assetbundles to the specified path.
        See download() for a list of keyword arguments.
        """
        objects = [ab for ab in self.assetbundles]
        self._do_download(objects, nworker, **kwargs)

    def download_all_resources(self, nworker: int = DEFAULT_DOWNLOAD_NWORKER, **kwargs):
        """
        Downloads all resources to the specified path.
        See download() for a list of keyword arguments.
        """
        objects = [res for res in self.resources]
        self._do_download(objects, nworker, **kwargs)

    def download_all(self, nworker: int = DEFAULT_DOWNLOAD_NWORKER, **kwargs):
        """
        Downloads all assetbundles and resources to the specified path.
        See download() for a list of keyword arguments.
        """
        # Instead of calling two separate methods,
        # this approach ensures all workers are busy at transition.
        objects = [ab for ab in self.assetbundles]
        objects.extend([res for res in self.resources])
        self._do_download(objects, nworker, **kwargs)

    def _do_download(self, objects: list, nworker: int, **kwargs):
        """
        [INTERNAL] Dispatches a list of objects to concurrent download tasks.
        """
        self.executor = ThreadPoolExecutor(max_workers=nworker)
        futures = [self.executor.submit(obj.download, **kwargs) for obj in objects]
        for future in as_completed(futures):
            future.result()
        self.executor.shutdown()
