"""
media/video.py
USM video conversion plugin for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

import base64
import ffmpeg
from pathlib import Path


logger = Logger()


class GkmasVideo(GkmasDummyMedia):

    def __init__(self, name: str, data: bytes):
        """
        Initializes a video using provided USM bytes.
        Raises a warning and falls back to raw dump if the video is not recognized.
        """

        super().__init__(name, data)

        try:
            stream_in = ffmpeg.input("pipe:0")
            stream_out = ffmpeg.output(
                stream_in,
                "pipe:1",
                vcodec="libx264",
                preset="ultrafast",
                format="mp4",
                movflags="frag_keyframe+empty_moov",
                # otherwise libx264 reports 'muxer does not support non seekable output'
            )
            self.obj, _ = ffmpeg.run(
                stream_out,
                input=data,
                capture_stdout=True,
                capture_stderr=True,
            )
        except:
            logger.warning(f"{name} is not recognized by ffmpeg, fallback to rawdump")
            self.valid = False

    def _get_embed_url(self) -> str:
        return f"data:video/mp4;base64,{base64.b64encode(self.obj).decode()}"

    def export(self, path: Path, convert_video: bool = True):

        if not (self.valid and convert_video):
            super().export(path)
            return

        path.with_suffix(".mp4").write_bytes(self.obj)
        logger.success(f"{self.name} downloaded and extracted as MP4")
