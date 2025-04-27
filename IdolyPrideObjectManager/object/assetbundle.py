"""
assetbundle.py
Unity asset bundle downloading, deobfuscation, and media extraction.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    UNITY_SIGNATURE,
)

from .resource import PrideResource
from .deobfuscate import PrideAssetBundleDeobfuscator
from ..media import PrideDummyMedia
from ..media.image import PrideUnityImage
from ..media.audio import PrideUnityAudio
from ..media.video import PrideUnityVideo

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

    def __init__(self, info: dict, url_template: str):
        """
        Initializes an assetbundle with the given information.
        Usually called from PrideManifest.

        Args:
            info (dict): An info dictionary, extracted from protobuf.
            url_template (str): URL template for downloading the assetbundle.
                {o} will be replaced with self.objectName,
                {g} with self.generation,
                {v} with self.uploadVersionId,
                and {type} with 'assetbundle'.
        """

        super().__init__(info, url_template)
        self._idname = f"AB[{self.id:05}] '{self.name}'"
        self._url = url_template.format(
            o=self.objectName,
            g=self.generation,
            v=self.uploadVersionId,
            type="assetbundle",
        )

    def __repr__(self):
        return f"<PrideAssetBundle {self._idname}>"

    def _get_media(self):
        """
        [INTERNAL] Instantiates a high-level media class based on the assetbundle name.
        Used to dispatch download and extraction.
        """

        if self._media is None:
            data = self._download_bytes()
            if self.name.startswith("img_") and "." not in self.name:
                media_class = PrideUnityImage
            elif self.name.startswith("spi_") and "." not in self.name:
                media_class = PrideUnityImage
            elif self.name.startswith("sud_"):
                media_class = PrideUnityAudio
            elif self.name.startswith("mov_") or self.name.startswith("adv_"):
                media_class = PrideUnityVideo
            else:
                media_class = PrideDummyMedia
            self._media = media_class(self._idname, data, int(self.generation))

        return self._media

    def _download_path(self, path: PATH_ARGTYPE, categorize: bool) -> Path:
        """
        [INTERNAL] Refines the download path based on user input.
        Inherited from PrideResource, but imposes a '.unity3d' suffix if no suffix is present.
        """
        p = super()._download_path(path, categorize)
        if p.suffix == "":
            return p.with_suffix(".unity3d")
        return p

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
