"""
plugins/audio.py
AWB audio extraction plugin for GkmasResource.
"""

from ...log import Logger

import subprocess
from io import BytesIO
from pathlib import Path
from pydub import AudioSegment


logger = Logger()


class AWBAudio:

    def __init__(
        self,
        name: str,
        data: bytes,
    ):
        """
        Initializes **one** AWB audio from raw resource bytes.
        Raises a warning and falls back to raw dump if the archive contains multiple tracks.
        """

        self.valid = True
        self.name = name
        self.io = BytesIO(data)
        self.io.seek(0)

    def extract(
        self,
        path: Path,
        audio_format: str,
    ):
        """
        Attempts to extract a single audio track from the archive.
        """

        subprocess.run(
            "vgmstream",
            input=self.io,
            stdout=path.open("wb"),
            check=True,
        )
