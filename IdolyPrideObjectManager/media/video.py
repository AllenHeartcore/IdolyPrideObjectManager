"""
media/video.py
MP4 video handler for PrideResource.
"""

import subprocess

import UnityPy

from .dummy import PrideDummyMedia


class PrideVideo(PrideDummyMedia):
    """Handler for videos of common formats recognized by FFmpeg."""

    def _init_mimetype(self):
        self.mimetype = "video"
        self.raw_format = self.ext

    def _convert(self, raw: bytes) -> bytes:

        return subprocess.run(
            [
                "ffmpeg",
                "-i",
                "pipe:0",  # input bytestream
                "-f",
                self.converted_format,
                "-preset",
                "ultrafast",
                "-movflags",
                "frag_keyframe+empty_moov",
                # otherwise libx264 reports 'muxer does not support non seekable output'
                "pipe:1",  # output bytestream
            ],
            input=raw,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # disposed
            check=True,
        ).stdout


class PrideUnityVideo(PrideVideo):
    """Conversion plugin for Unity video."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.raw_format = None  # don't override
        self.default_converted_format = "mp4"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        assert len(values) == 1, f"{self.name} contains {len(values)} video clips."
        data = values[0].read().m_VideoData.tobytes()
        return data if self.converted_format == "mp4" else super()._convert(data)
