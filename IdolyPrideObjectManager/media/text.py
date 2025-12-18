"""
media/text.py
Unity text conversion plugin for PrideAssetBundle.
"""

import UnityPy

from .dummy import PrideDummyMedia


class PrideUnityText(PrideDummyMedia):
    """Conversion plugin for Unity text."""

    def _init_mimetype(self):
        self.mimetype = "text"
        self.default_converted_format = self.ext

    def _convert(self, raw: bytes) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        if len(values) != 1:
            self.reporter.error(f"Contains {len(values)} TextAsset's, expected 1.")
        return values[0].read().m_Script.encode("utf-8")
