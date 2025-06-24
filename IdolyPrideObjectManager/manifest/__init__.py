"""
manifest/
Manifest (object database) management.
Entry point of the IdolyPrideObjectManager package.
"""

import json
from pathlib import Path
from urllib.parse import urljoin

import requests
from google.protobuf.message import DecodeError

from ..const import (
    PRIDE_API_HEADER,
    PRIDE_API_URL,
    PRIDE_OCTOCACHE_IV,
    PRIDE_OCTOCACHE_KEY,
    PRIDE_ONLINEPDB_IV,
    PRIDE_ONLINEPDB_KEY,
    PathArgtype,
)
from .decrypt import AESCBCDecryptor
from .manifest import PrideManifest
from .octodb_pb2 import pdbytes2dict


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
    req = requests.get(url, headers=PRIDE_API_HEADER, timeout=10)
    req.raise_for_status()  # Raise an error for bad responses
    enc = req.content
    dec = AESCBCDecryptor(PRIDE_ONLINEPDB_KEY, PRIDE_ONLINEPDB_IV).process(enc)
    return PrideManifest(pdbytes2dict(dec[16:]), base_revision=base_revision)


def load(src: PathArgtype, base_revision: int = 0) -> PrideManifest:
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
            **Must be manually specified if loading a diff generated
            by IdolyPrideObjectManager older than or equal to v0.4-beta.**
    """
    try:
        return PrideManifest(
            json.loads(Path(src).read_text(encoding="utf-8")),
            base_revision,
        )
    except json.JSONDecodeError:
        enc = Path(src).read_bytes()
        try:
            return PrideManifest(pdbytes2dict(enc), base_revision)
        except DecodeError:
            dec = AESCBCDecryptor(PRIDE_OCTOCACHE_KEY, PRIDE_OCTOCACHE_IV).process(enc)
            return PrideManifest(pdbytes2dict(dec[16:]), base_revision)  # trim md5 hash
