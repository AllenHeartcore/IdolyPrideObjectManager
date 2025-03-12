"""
media/audio.py
AWB/ACB audio conversion plugin for GkmasResource,
and MP3 audio handler for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

import UnityPy


logger = Logger()


class GkmasAudio(GkmasDummyMedia):
    """Handler for audio of common formats."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.mimetype = "audio"
        self.raw_format = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        return raw


class GkmasUnityAudio(GkmasAudio):
    """Conversion plugin for Unity audio."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.raw_format = None  # don't override
        self.converted_format = "wav"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        assert len(values) == 1, f"{self.name} contains {len(values)} audio clips."
        samples = values[0].read().samples
        sample = list(samples.values())[0]
        return sample if self.converted_format == "wav" else super()._convert(sample)
        # UnityPy is decompressing AudioClip into clean PCM bytes for us
