"""
media/video.py
MP4 video handler for PrideResource.
"""

from ..log import Logger
from .dummy import PrideDummyMedia

from pathlib import Path

import ffmpeg


logger = Logger()


class PrideVideo(PrideDummyMedia):
    """Handler for videos of common formats recognized by FFmpeg."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.mimetype = "video"
        self.raw_format = "mp4"

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
