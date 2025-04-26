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

from .resource import PrideResource
from .deobfuscate import PrideAssetBundleDeobfuscator
from ..media import PrideDummyMedia
from ..media.image import PrideUnityImage
from ..media.audio import PrideUnityAudio

from pathlib import Path


logger = Logger()


class PrideAssetBundle(PrideResource):
    """
    An assetbundle. Class inherits from PrideResource.

    Attributes:
        All attributes from PrideResource, plus
        name (str): Human-readable name.
            Appended with '.unity3d' only at download and CSV export.
        crc (int): CRC checksum, unused for now (since scheme is unknown).

    Methods:
        download(
            path: Union[str, Path] = DEFAULT_DOWNLOAD_PATH,
            categorize: bool = True,
            convert_image: bool = True,
            image_format: str = "png",
            image_resize: Union[None, str, Tuple[int, int]] = None,
        ) -> None:
            Downloads and deobfuscates the assetbundle to the specified path.
            Also extracts a single image from each bundle with type 'img'.
    """

    def __init__(self, info: dict):
        """
        Initializes an assetbundle with the given information.
        Usually called from PrideManifest.

        Args:
            info (dict): An info dictionary, extracted from protobuf.
                Must contain the following keys: id, name, objectName, size, md5, state, crc.
        """

        super().__init__(info)
        self.crc = info["crc"]  # unused (for now)
        self.dependencies = info.get("dependencies", [])
        self._idname = f"AB[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<PrideAssetBundle {self._idname}>"

    def _get_canon_repr(self):
        ret = {field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_HEAD}
        ret["crc"] = self.crc
        if self.dependencies:
            ret["dependencies"] = self.dependencies  # for ordering
        ret.update({field: getattr(self, field) for field in RESOURCE_INFO_FIELDS_TAIL})
        return ret

    def _get_media(self):
        """
        [INTERNAL] Instantiates a high-level media class based on the assetbundle name.
        Used to dispatch download and extraction.
        """

        if self._media is None:
            data = self._download_bytes()
            if self.name.startswith("img_"):
                media_class = PrideUnityImage
            elif self.name.startswith("sud_"):
                media_class = PrideUnityAudio
            else:
                media_class = PrideDummyMedia
            self._media = media_class(self._idname, data, self._mtime)

        return self._media

    def _download_path(self, path: PATH_ARGTYPE, categorize: bool) -> Path:
        """
        [INTERNAL] Refines the download path based on user input.
        Inherited from PrideResource, but imposes a '.unity3d' suffix.
        """
        return super()._download_path(path, categorize).with_suffix(".unity3d")

    def _download_bytes(self) -> bytes:
        """
        [INTERNAL] Downloads, and optionally deobfuscates, the assetbundle as raw bytes.
        Sanity checks are implemented in parent class PrideResource.
        """

        data = super()._download_bytes()

        if not data.startswith(UNITY_SIGNATURE):
            data = PrideAssetBundleDeobfuscator(self.name).process(data)
            if not data.startswith(UNITY_SIGNATURE):
                logger.warning(f"{self._idname} downloaded but LEFT OBFUSCATED")
                # Unexpected things may happen...
                # So unlike _download_bytes(), here we don't raise an error and abort.

        return data
