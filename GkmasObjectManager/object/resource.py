"""
resource.py
General-purpose resource downloading.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    IMG_RESIZE_ARGTYPE,
    DEFAULT_DOWNLOAD_PATH,
    GKMAS_OBJECT_SERVER,
    CHARACTER_ABBREVS,
)

import re
import requests
from hashlib import md5
from pathlib import Path
from urllib.parse import urljoin


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
        **kwargs,
    ):
        """
        Downloads the resource to the specified path.

        Args:
            path (Union[str, Path]) = DEFAULT_DOWNLOAD_PATH: A directory or a file path.
                If a directory, subdirectories are auto-determined based on the resource name.
            categorize (bool) = True: Whether to put the downloaded object into subdirectories.
                If False, the object is directly downloaded to the specified 'path'.
        """

        path = self._download_path(path, categorize)
        if path.exists():
            logger.warning(f"{self._idname} already exists")
            return

        dec = self._download_bytes()
        path.write_bytes(dec)
        logger.success(f"{self._idname} downloaded")

    def _download_path(self, path: PATH_ARGTYPE, categorize: bool) -> Path:
        """
        [INTERNAL] Refines the download path based on user input.
        Appends subdirectories unless a definite file path (with suffix) is given.
        Delimiter is hardcoded as '_'.

        path is not necessarily of type Path,
        since we don't expect the client to import pathlib in advance.

        Example:
            path = 'out/' and self.name = 'type_subtype-detail.ext'
            will be refined to 'out/type/subtype/type_subtype-detail.ext'
            if categorize is True, and 'out/type_subtype-detail.ext' otherwise.
        """

        path = Path(path)

        if path.suffix == "":  # is directory
            if categorize:
                path = path / self._determine_subdir(self.name) / self.name
            else:
                path = path / self.name

        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _determine_subdir(self, filename: str) -> Path:
        """
        [INTERNAL] Automatically organize files into nested subdirectories,
        stopping at the first 'character identifier'.
        """

        filename = Path(filename).stem  # remove extension

        # Ignore everything after the first number after '-' or '_'
        filename = re.split(r"[-_]\d", filename)[0]

        for char in CHARACTER_ABBREVS:
            if char in filename:
                # Ignore everything after 'char', and trim trailing '-' or '_'
                filename = filename.split(char)[0] + char
                break

        return Path(*filename.split("_"))

    def _download_bytes(self) -> bytes:
        """
        [INTERNAL] Downloads the resource from the server and performs sanity checks
        on HTTP status code, size, and MD5 hash. Returns the resource as raw bytes.
        """

        url = urljoin(GKMAS_OBJECT_SERVER, self.objectName)
        response = requests.get(url)

        # We're being strict here by aborting the download process
        # if any of the sanity checks fail, in order to avoid corrupted output.
        # The client can always retry; just ignore the "file already exists" warnings.
        # Note: Returning empty bytes is unnecessary, since logger.error() raises an exception.

        if response.status_code != requests.codes.ok:
            logger.error(
                f"{self._idname} request failed with {response.status_code}: {response.reason}"
            )

        if len(response.content) != self.size:
            logger.error(f"{self._idname} has invalid size")

        if md5(response.content).hexdigest() != self.md5:
            logger.error(f"{self._idname} has invalid MD5 hash")

        return response.content
