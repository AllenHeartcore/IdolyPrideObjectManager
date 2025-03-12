"""
assetbundle.py
Asset bundle downloading, deobfuscation, and media extraction.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    RESOURCE_INFO_FIELDS_HEAD,
    RESOURCE_INFO_FIELDS_TAIL,
    DEFAULT_DOWNLOAD_PATH,
)

from .resource import GkmasResource
from .deobfuscate import GkmasAssetBundleDeobfuscator
from ..media import GkmasDummyMedia

from pathlib import Path


logger = Logger()


class GkmasAssetBundle(GkmasResource):
    """
    An assetbundle. Class inherits from GkmasResource.

    Attributes:
        All attributes from GkmasResource, plus
        name (str): Human-readable name.
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

    def _get_media(self):
        """
        [INTERNAL] Instantiates a high-level media class based on the assetbundle name.
        Used to dispatch download and extraction.
        """

        if self._media is None:
            data = self._download_bytes()
            self._media = GkmasDummyMedia(self._idname, data)

        return self._media

    def _download_bytes(self) -> bytes:
        """
        [INTERNAL] Downloads, and optionally deobfuscates, the assetbundle as raw bytes.
        Sanity checks are implemented in parent class GkmasResource.
        """

        data = super()._download_bytes()
        data = GkmasAssetBundleDeobfuscator(self.name).process(data)
        return data
