"""
_download.py
[CLASS SPLIT] GkmasAssetBundle and GkmasResource downloading.
"""

from ..log import Logger
from ..const import (
    PATH_ARGTYPE,
    GKMAS_OBJECT_SERVER,
    CHARACTER_ABBREVS,
)

import re
import requests
from hashlib import md5
from pathlib import Path
from urllib.parse import urljoin


logger = Logger()


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

    filename = ".".join(filename.split(".")[:-1])  # remove extension

    # Ignore everything after the first number after '-' or '_'
    filename = re.split(r"[-_]\d", filename)[0]

    for char in CHARACTER_ABBREVS:
        if char in filename:
            # Ignore everything after 'char', and trim trailing '_' or '-'
            filename = filename.split(char)[0][:-1]
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
    # The client can always retry (just ignore the "file already exists" warnings).
    # Note: Returning empty bytes is unnecessary, since logger.error() raises an exception.

    if response.status_code != 200:
        logger.error(f"{self._idname} download failed")

    if len(response.content) != self.size:
        logger.error(f"{self._idname} has invalid size")

    if md5(response.content).hexdigest() != self.md5:
        logger.error(f"{self._idname} has invalid MD5 hash")

    return response.content
