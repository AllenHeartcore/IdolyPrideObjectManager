"""
adv/adventure.py
Adventure (story script) plugin for PrideResource.
"""

from ..log import Logger
from ..media import PrideDummyMedia
from .parser import PradvCommandParser

import json


logger = Logger()
parser = PradvCommandParser()


class PrideAdventure(PrideDummyMedia):
    """Handler for adventure story scripts."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.mimetype = "text"
        self.converted_format = "json"

        self.commands = [
            parser.process(line) for line in raw.decode("utf-8").splitlines()
        ]

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        # only for compatibility with PrideResource
        return bytes(
            json.dumps(
                self.commands,
                indent=4,
                ensure_ascii=False,
            ),
            "utf-8",
        )
