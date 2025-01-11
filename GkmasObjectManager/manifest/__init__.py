from ..const import (
    PATH_ARGTYPE,
    GKMAS_API_URL,
    GKMAS_API_HEADER,
    GKMAS_ONLINEPDB_KEY,
    GKMAS_OCTOCACHE_KEY,
    GKMAS_OCTOCACHE_IV,
)

from .manifest import GkmasManifest
from .decrypt import AESCBCDecryptor
from .octodb_pb2 import pdbytes2dict

import json
import requests
from pathlib import Path
from urllib.parse import urljoin


def fetch(revision: int = 0) -> GkmasManifest:
    """
    Requests an online manifest by the specified revision.
    Algorithm courtesy of github.com/DreamGallery/HatsuboshiToolkit
    """
    url = urljoin(GKMAS_API_URL, str(revision))
    enc = requests.get(url, headers=GKMAS_API_HEADER).content
    dec = AESCBCDecryptor(GKMAS_ONLINEPDB_KEY, enc[:16]).process(enc[16:])
    return GkmasManifest(pdbytes2dict(dec))


def load(src: PATH_ARGTYPE):
    """
    Initializes a manifest from the given offline source.
    The protobuf referred to can be either encrypted or not.
    Also supports importing from JSON.

    Args:
        src (Union[str, Path]): Path to the manifest file.
            Can be the path to
            - an encrypted octocache (usually named 'octocacheevai'),
            - a decrypted protobuf, or
            - a JSON file exported from another manifest.
    """
    try:
        return GkmasManifest(json.loads(Path(src).read_text()))
    except:
        enc = Path(src).read_bytes()
        try:
            return GkmasManifest(pdbytes2dict(enc))
        except:
            dec = AESCBCDecryptor(GKMAS_OCTOCACHE_KEY, GKMAS_OCTOCACHE_IV).process(enc)
            return GkmasManifest(pdbytes2dict(dec[16:]))  # trim md5 hash
