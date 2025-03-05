"""
media/audio.py
AWB audio extraction plugin for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

import base64
import subprocess
from io import BytesIO
from pathlib import Path
from pydub import AudioSegment


logger = Logger()


class GkmasAudio(GkmasDummyMedia):

    def __init__(self, name: str, data: bytes):
        """
        Initializes **one** audio of common formats recognized by pydub.
        Raises a warning and falls back to raw dump if the audio is not recognized.
        """

        super().__init__(name, data)

        try:
            self.obj = AudioSegment.from_file(BytesIO(data))
        except:
            logger.warning(f"{name} is not recognized by pydub, fallback to rawdump")
            # fallback case is handled within parent class

    def _get_embed_url(self) -> str:
        # 'self.name' is actually 'self._idname' in object, therefore the name is enclosed in quotes
        return f"data:audio/{self.name.split('.')[-1][:-1]};base64,{base64.b64encode(self.data).decode()}"


class GkmasAWBAudio(GkmasAudio):

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

    def _get_embed_url(self) -> str:
        return ""

    def export(
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
