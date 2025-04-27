"""
media/video.py
MP4 video handler for PrideResource.
"""

from ..log import Logger
from .dummy import PrideDummyMedia

from pathlib import Path

import ffmpeg
import UnityPy


logger = Logger()


class PrideVideo(PrideDummyMedia):
    """Handler for videos of common formats recognized by FFmpeg."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.mimetype = "video"
        self.raw_format = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes, **kwargs) -> bytes:

        stream_in = ffmpeg.input("pipe:0")
        stream_out = ffmpeg.output(
            stream_in,
            "pipe:1",
            preset="ultrafast",
            format=self.converted_format,
            movflags="frag_keyframe+empty_moov",
            # otherwise libx264 reports 'muxer does not support non seekable output'
        )

        return ffmpeg.run(
            stream_out,
            input=raw,
            capture_stdout=True,
            capture_stderr=True,
        )[0]


class PrideUnityVideo(PrideVideo):
    """Conversion plugin for Unity video."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.raw_format = None  # don't override
        self.converted_format = "mp4"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        assert len(values) == 1, f"{self.name} contains {len(values)} video clips."
        data = values[0].read().m_VideoData.tobytes()
        return data if self.converted_format == "mp4" else super()._convert(data)
