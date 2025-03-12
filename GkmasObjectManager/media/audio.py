"""
media/audio.py
AWB/ACB audio conversion plugin for GkmasResource,
and MP3 audio handler for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia


logger = Logger()


class GkmasAudio(GkmasDummyMedia):
    """Handler for audio of common formats."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.mimetype = "audio"
        self.raw_format = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        return raw
