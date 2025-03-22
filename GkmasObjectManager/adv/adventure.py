"""
adv/adventure.py
Adventure (story script) plugin for GkmasResource.
"""

from ..log import Logger
from ..media import GkmasDummyMedia
from .parser import GkadvCommandParser

import json


logger = Logger()
parser = GkadvCommandParser()


class GkmasAdventure(GkmasDummyMedia):
    """Handler for adventure story scripts."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.mimetype = "text"
        self.converted_format = "json"

        self.commands = parser.process(raw.decode("utf-8"))

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        # only for compatibility with GkmasResource
        return bytes(json.dumps(self.commands), "utf-8")
