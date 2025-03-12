from ..const import PATH_ARGTYPE

from .manifest import GkmasManifest

import json
from pathlib import Path


def load(src: PATH_ARGTYPE, base_revision: int = 0) -> GkmasManifest:
    """
    Initializes a manifest from the given offline source.
    Also supports importing from JSON.

    Args:
        src (Union[str, Path]): Path to a JSON file exported from another manifest.
        base_revision (int) = 0: The revision number of the base manifest.
            **Must be manually specified if loading a diff genereated
            by GkmasObjectManager older than or equal to v0.4-beta.**
    """
    return GkmasManifest(json.loads(Path(src).read_text()), base_revision)
