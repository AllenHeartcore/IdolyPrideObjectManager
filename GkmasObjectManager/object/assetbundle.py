"""
assetbundle.py
Unity asset bundle downloading, deobfuscation, and media extraction.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    RESOURCE_INFO_FIELDS_HEAD,
    RESOURCE_INFO_FIELDS_TAIL,
    DEFAULT_DOWNLOAD_PATH,
    UNITY_SIGNATURE,
)

from .resource import GkmasResource
from .deobfuscate import GkmasAssetBundleDeobfuscator
from .plugins.image import UnityImage


logger = Logger()


class GkmasAssetBundle(GkmasResource):
    """
    An assetbundle. Class inherits from GkmasResource.

    Attributes:
        All attributes from GkmasResource, plus
        name (str): Human-readable name.
            Appended with '.unity3d' only at download and CSV export.
        crc (int): CRC checksum, unused for now (since scheme is unknown).

    Methods:
        download(
            path: Union[str, Path] = DEFAULT_DOWNLOAD_PATH,
            categorize: bool = True,
            extract_img: bool = True,
            img_format: str = "png",
            img_resize: Union[None, str, Tuple[int, int]] = None,
        ) -> None:
            Downloads and deobfuscates the assetbundle to the specified path.
            Also extracts a single image from each bundle with type 'img'.
    """

    def __init__(self, info: dict):
        """
        Initializes an assetbundle with the given information.
        Usually called from GkmasManifest.

        Args:
            info (dict): An info dictionary, extracted from protobuf.
                Must contain the following keys: id, name, objectName, size, md5, state, crc.
        """

        super().__init__(info)
        self.crc = info["crc"]  # unused (for now)
        self.dependencies = info.get("dependencies", [])
        self._idname = f"AB[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<GkmasAssetBundle {self._idname}>"

    def _get_canon_repr(self):
        ret = {field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_HEAD}
        ret["crc"] = self.crc
        if self.dependencies:
            ret["dependencies"] = self.dependencies  # for ordering
        ret.update({field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_TAIL})
        return ret

    def download(
        self,
        path: PATH_ARGTYPE = DEFAULT_DOWNLOAD_PATH,
        categorize: bool = True,
        **kwargs,
    ):
        """
        Downloads and deobfuscates the assetbundle to the specified path.

        Args:
            path (Union[str, Path]) = DEFAULT_DOWNLOAD_PATH: A directory or a file path.
                If a directory, subdirectories are auto-determined based on the assetbundle name.
            categorize (bool) = True: Whether to put the downloaded object into subdirectories.
                If False, the object is directly downloaded to the specified 'path'.
            extract_img (bool) = True: Whether to extract a single image from assetbundles of type 'img'.
                If False, 'img_.*\\.unity3d' is downloaded as is.
            img_format (str) = 'png': Image format for extraction. Case-insensitive.
                Effective only when 'extract_img' is True.
                Valid options are checked by PIL.Image.save() and are not enumerated.
            img_resize (Union[None, str, Tuple[int, int]]) = None: Image resizing argument.
                If None, image is downloaded as is.
                If str, string must contain exactly one ':' and image is resized to the specified ratio.
                If Tuple[int, int], image is resized to the specified exact dimensions.
        """

        path = self._download_path(path, categorize).with_suffix(".unity3d")
        if path.exists():
            logger.warning(f"{self._idname} already exists")
            return

        enc = self._download_bytes()

        if enc.startswith(UNITY_SIGNATURE):
            self._extract_dispatcher(path, enc, **kwargs)
        else:
            dec = GkmasAssetBundleDeobfuscator(self.name).process(enc)
            if dec.startswith(UNITY_SIGNATURE):
                self._extract_dispatcher(path, dec, **kwargs)
            else:
                path.write_bytes(enc)
                logger.warning(f"{self._idname} downloaded but LEFT OBFUSCATED")
                # Unexpected things may happen...
                # So unlike _download_bytes() in the parent class,
                # here we don't raise an error and abort.

    def _extract_dispatcher(
        self,
        path: PATH_ARGTYPE,  # no default value to enforce presence
        data: bytes,
        **kwargs,
    ):
        """
        [INTERNAL] Dispatches the extraction of various formats
        based on the assetbundle's name and the extract_* flags.
        Designed to be modular and easily extensible.
        **Also this is where kwargs are actually parsed.**
        """

        if self.name.startswith("img_") and kwargs.get("extract_img", True):
            UnityImage(self._idname, data).extract(
                path,
                img_format=kwargs.get("img_format", "png"),
                img_resize=kwargs.get("img_resize", None),
                # caller-side kwargs parsing enforces callee-side type checking
            )
        else:
            path.write_bytes(data)
            logger.success(f"{self._idname} downloaded")
