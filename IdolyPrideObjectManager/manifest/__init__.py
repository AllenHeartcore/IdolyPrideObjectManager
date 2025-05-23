from ..const import (
    PATH_ARGTYPE,
    PRIDE_API_URL,
    PRIDE_API_HEADER,
    PRIDE_ONLINEPDB_KEY,
    PRIDE_ONLINEPDB_IV,
    PRIDE_OCTOCACHE_KEY,
    PRIDE_OCTOCACHE_IV,
)

from .manifest import PrideManifest
from .decrypt import AESCBCDecryptor
from .octodb_pb2 import pdbytes2dict

import json
import requests
from pathlib import Path
from urllib.parse import urljoin


def fetch(base_revision: int = 0) -> PrideManifest:
    """
    Requests an online manifest by the specified revision.
    Algorithm courtesy of github.com/DreamGallery/HatsuboshiToolkit

    Args:
        base_revision (int): The "base" revision number of the manifest.
            This API return the *difference* between the specified base
            revision and the latest. Defaults to 0 (standalone latest).
    """
    url = urljoin(PRIDE_API_URL, str(base_revision))
    enc = requests.get(url, headers=PRIDE_API_HEADER).content
    dec = AESCBCDecryptor(PRIDE_ONLINEPDB_KEY, PRIDE_ONLINEPDB_IV).process(enc)
    return PrideManifest(pdbytes2dict(dec[16:]), base_revision=base_revision)


def load(src: PATH_ARGTYPE, base_revision: int = 0) -> PrideManifest:
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
        base_revision (int) = 0: The revision number of the base manifest.
            **Must be manually specified if loading a diff genereated
            by IdolyPrideObjectManager older than or equal to v0.4-beta.**
    """
    try:
        return PrideManifest(json.loads(Path(src).read_text()), base_revision)
    except:
        enc = Path(src).read_bytes()
        try:
            return PrideManifest(pdbytes2dict(enc), base_revision)
        except:
            dec = AESCBCDecryptor(PRIDE_OCTOCACHE_KEY, PRIDE_OCTOCACHE_IV).process(enc)
            return PrideManifest(pdbytes2dict(dec[16:]), base_revision)  # trim md5 hash
