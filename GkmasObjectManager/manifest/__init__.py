from ..const import PATH_ARGTYPE

from .manifest import GkmasManifest
from .octodb_pb2 import pdbytes2dict

import json
from pathlib import Path


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
