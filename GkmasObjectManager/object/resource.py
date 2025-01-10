"""
resource.py
General-purpose resource downloading.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    IMG_RESIZE_ARGTYPE,
    DEFAULT_DOWNLOAD_PATH,
)


logger = Logger()


class GkmasResource:
    """
    A general-purpose binary resource, presumably multimedia instead of an assetbundle.

    Attributes:
        id (int): Resource ID, unique across manifests.
        name (str): Human-readable name, unique across manifests.
        objectName (str): Object name on server, 6-character alphanumeric.
        size (int): Resource size in bytes, used for integrity check.
        md5 (str): MD5 hash of the resource, used for integrity check.
        state (str): Resource state in manifest (ADD/UPDATE), unused for now.
            Other possible states of NONE, LATEST, and DELETE have not yet been observed.

    Methods:
        download(
            path: Union[str, Path] = DEFAULT_DOWNLOAD_PATH,
            categorize: bool = True,
        ) -> None:
            Downloads the resource to the specified path.
    """

    from ._download import _download_path, _download_bytes, _determine_subdir

    def __init__(self, info: dict):
        """
        Initializes a resource with the given information.
        Usually called from GkmasManifest.

        Args:
            info (dict): An info dictionary, extracted from protobuf.
                Must contain the following keys: id, name, objectName, size, md5, state.
        """

        self.id = info["id"]
        self.name = info["name"]
        self.size = info["size"]
        self.state = info["state"]  # unused
        self.md5 = info["md5"]
        self.objectName = info["objectName"]
        self._idname = f"RS[{self.id:05}] '{self.name}'"

    def __repr__(self):
        return f"<GkmasResource {self._idname}>"

    def download(
        self,
        path: PATH_ARGTYPE = DEFAULT_DOWNLOAD_PATH,
        categorize: bool = True,
        extract_img: bool = True,
        img_format: str = "png",
        img_resize: IMG_RESIZE_ARGTYPE = None,
    ):
        """
        Downloads the resource to the specified path.

        Args:
            path (Union[str, Path]) = DEFAULT_DOWNLOAD_PATH: A directory or a file path.
                If a directory, subdirectories are auto-determined based on the resource name.
            categorize (bool) = True: Whether to put the downloaded object into subdirectories.
                If False, the object is directly downloaded to the specified 'path'.
            extract_img (bool) = True:
                IGNORED. PRESERVED FOR COMPATIBILITY WITH CONCURRENT DOWNLOADER.
            img_format (str) = 'png':
                IGNORED. PRESERVED FOR COMPATIBILITY WITH CONCURRENT DOWNLOADER.
            img_resize (Union[None, str, Tuple[int, int]]) = None:
                IGNORED. PRESERVED FOR COMPATIBILITY WITH CONCURRENT DOWNLOADER.
        """

        path = self._download_path(path, categorize)
        if path.exists():
            logger.warning(f"{self._idname} already exists")
            return

        dec = self._download_bytes()
        path.write_bytes(dec)
        logger.success(f"{self._idname} downloaded")
