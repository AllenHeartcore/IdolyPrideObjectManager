"""
manifest.py
Manifest decryption, exporting, and object downloading.
"""

from ..log import Logger
from ..const import PATH_ARGTYPE, DICLIST_IGNORED_FIELDS


# The logger would better be a global variable in the
# modular __init__.py, but Python won't allow me to
logger = Logger()


class GkmasManifest:
    """
    A GKMAS manifest, containing info about assetbundles and resources.

    Attributes:
        raw (bytes): Raw decrypted protobuf bytes.
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
    from ._initdb import _online_init, _offline_init, _parse_raw, _parse_jdict
    from ._download import download
    from ._export import export, _export_pdb, _export_json, _export_csv

    def __init__(self, src: PATH_ARGTYPE = None):
        """
        Initializes a manifest from the given source.
        Only performs decryption when necessary, and
        leaves protobuf parsing to internal backend.

        Args:
            src (Union[str, Path]): Path to the manifest file.
                Can be the path to an encrypted octocache
                (usually named 'octocacheevai') or a decrypted protobuf.
                If None, an empty manifest is created (used for manifest from diff;
                note that _parse_jdict() must be manually called afterwards).
        """

        if not src:  # empty constructor
            self.revision = None
            return

        if isinstance(src, str) and src.startswith("<") and src.endswith(">"):
            self._online_init(int(src[1:-1]))
        else:
            self._offline_init(src)

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
