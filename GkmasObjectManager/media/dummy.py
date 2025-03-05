"""
media/dummy.py
Dummy media extraction plugin.
Serves as a fallback for unknown media types,
as well as a base class & template for other media plugins.
"""

from ..log import Logger

from pathlib import Path


logger = Logger()


class GkmasDummyMedia:

    def __init__(
        self,
        name: str,
        data: bytes,
    ):
        self.valid = True
        self.name = name  # only for logging
        self.obj = data

    def _get_embed_url(self) -> str:
        return ""

    def caption(self) -> str:
        return "[Captioning not supported for raw binary data.]"

    def export(
        self,
        path: Path,
    ):
        path.write_bytes(self.obj)
        logger.success(f"{self.name} downloaded")
