"""
assetbundle.py
Unity asset bundle downloading, deobfuscation, and media extraction.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    IMG_RESIZE_ARGTYPE,
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
            Appended with '.unity3d' only at CSV export.
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
        self._idname = f"AB[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<GkmasAssetBundle {self._idname}>"

    def download(
        self,
        path: PATH_ARGTYPE = DEFAULT_DOWNLOAD_PATH,
        categorize: bool = True,
        extract_img: bool = True,
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

        path = self._download_path(path, categorize)
        if path.exists():
            logger.warning(f"{self._idname} already exists")
            return

        enc = self._download_bytes()

        if enc.startswith(UNITY_SIGNATURE):
            self._extract_dispatcher(path, enc, extract_img, **kwargs)
            logger.success(f"{self._idname} downloaded")
        else:
            dec = GkmasAssetBundleDeobfuscator(self.name).process(enc)
            if dec.startswith(UNITY_SIGNATURE):
                self._extract_dispatcher(path, dec, extract_img, **kwargs)
                logger.success(f"{self._idname} downloaded and deobfuscated")
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
        extract_img: bool,  # kwargs referenced in THIS method must be explicitly listed
        **kwargs,
    ):
        """
        [INTERNAL] Dispatches the extraction of various formats
        based on the assetbundle's name and the extract_* flags.
        Designed to be modular and easily extensible.
        """

        if self.name.startswith("img_") and extract_img:
            UnityImage(self._idname, data).export(path, **kwargs)
        else:
            path.write_bytes(data)
