"""
assetbundle.py
Unity asset bundle downloading, deobfuscation, and media extraction.
"""

from ..const import UNITY_SIGNATURE
from ..media import PrideDummyMedia
from ..media.audio import PrideUnityAudio
from ..media.image import PrideUnityImage
from ..media.video import PrideUnityVideo
from ..rich import ProgressReporter
from .deobfuscate import PrideAssetBundleDeobfuscator
from .resource import PrideResource


class PrideAssetBundle(PrideResource):
    """
    An assetbundle. Class inherits from PrideResource.

    Attributes:
        All attributes from PrideResource, plus
        name (str): Human-readable name, appended with '.unity3d'.
        crc (int): CRC checksum, unused for now (since scheme is unknown).

    Methods:
        download(
            path: Union[str, Path] = DEFAULT_DOWNLOAD_PATH,
            categorize: bool = True,
            **kwargs,
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
        self.name += ".unity3d"
        self._idname = f"AB[{self.id:05}] '{self.name}'"
        self._url = url_template.format(
            o=self.objectName,
            g=self.generation,
            v=self.uploadVersionId,
            type="assetbundle",
        )
        self._reporter = ProgressReporter(title=self._idname, total=self.size)
        # need to re-instantiate since self._idname has changed

    def __repr__(self) -> str:
        return f"<PrideAssetBundle {self._idname}>"

    @property
    def canon_repr(self) -> dict:
        canon = super().canon_repr
        canon["name"] = canon["name"].replace(".unity3d", "")
        return canon

    @property
    def _media_class(self) -> type:
        if self.name.startswith("img_"):
            return PrideUnityImage
        elif self.name.startswith("spi_"):
            return PrideUnityImage
        elif self.name.startswith("sud_"):
            return PrideUnityAudio
        elif self.name.startswith("mov_") or self.name.startswith("adv_"):
            return PrideUnityVideo
        else:
            return PrideDummyMedia

    def _download_bytes(self) -> dict:
        """
        [INTERNAL] Downloads, and optionally deobfuscates, the assetbundle as raw bytes.
        Sanity checks are implemented in parent class PrideResource.
        """

        data = super()._download_bytes()
        _bytes, _mtime = data["bytes"], data["mtime"]

        if not _bytes.startswith(UNITY_SIGNATURE):
            self._reporter.update("Deobfuscating")
            _bytes = PrideAssetBundleDeobfuscator(self.name).process(_bytes)
            if not _bytes.startswith(UNITY_SIGNATURE):
                self._reporter.warning("Downloaded but LEFT OBFUSCATED")
                # Unexpected things may happen...
                # So unlike _download_bytes(), here we don't raise an error and abort.

        return {
            "bytes": _bytes,
            "mtime": _mtime,
        }
