from ..const import (
    PATH_ARGTYPE,
    GKMAS_API_URL,
    GKMAS_API_HEADER,
    GKMAS_ONLINEPDB_KEY,
    GKMAS_OCTOCACHE_KEY,
    GKMAS_OCTOCACHE_IV,
)

from .manifest import GkmasManifest
from .octodb_pb2 import pdbytes2dict

import json
import requests
from pathlib import Path
from urllib.parse import urljoin


def fetch(revision: int = 0) -> GkmasManifest:
    """
    Requests an online manifest by the specified revision.
    Algorithm courtesy of github.com/DreamGallery/HatsuboshiToolkit

    Args:
        revision (int): The "base" revision number of the manifest.
            This API return the *difference* between the requested revision
            and the latest. Defaults to 0 (latest).
    """
    url = urljoin(GKMAS_API_URL, str(revision))
    dec = requests.get(url, headers=GKMAS_API_HEADER).content
    return GkmasManifest(pdbytes2dict(dec), base_revision=revision)


def load(src: PATH_ARGTYPE, base_revision: int = 0) -> GkmasManifest:
    """
    Initializes a manifest from the given offline source.
    Also supports importing from JSON.

    Args:
        src (Union[str, Path]): Path to the manifest file.
            Can be the path to
            - a protobuf (usually named 'octocacheevai'), or
            - a JSON file exported from another manifest.
        base_revision (int) = 0: The revision number of the base manifest.
            **Must be manually specified if loading a diff genereated
            by GkmasObjectManager older than or equal to v0.4-beta.**
    """
    try:
        return GkmasManifest(json.loads(Path(src).read_text()), base_revision)
    except:
        dec = Path(src).read_bytes()
        return GkmasManifest(pdbytes2dict(dec), base_revision)
