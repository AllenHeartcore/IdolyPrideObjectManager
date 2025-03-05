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

    def __init__(self, name: str, data: bytes):
        """
        Initializes **one** AWB audio from raw resource bytes.
        Raises a warning and falls back to raw dump if the archive contains multiple tracks.
        """

        super().__init__(name, data)

        self.obj = BytesIO(data)
        self.obj.seek(0)
        # It would be more reasonable to let self.obj be an AudioSegment,
        # but the AWB format is not directly supported by pydub.

        # Overwriting self.obj at conversion-enabled export is also bad for consistency, ...
        self.wav = None  # ... but having a separate attribute is a valid workaround.

    def _get_embed_url(self) -> str:
        return ""

    def export(
        self,
        path: Path,
        extract_audio: bool = True,
        audio_format: str = "wav",
    ):
        """
        Attempts to extract a single audio track from the archive.

        Args:
            extract_audio (bool) = True: Whether to extract a single audio track from the archive.
                If False, 'sud_.*\\.awb/acb' is downloaded as is.
                There are also cases where the audio is readily encoded in MP3.
            audio_format (str) = 'wav': Audio format for extraction. Case-insensitive.
                Effective only when 'extract_audio' is True.
                Valid options are checked by pydub.AudioSegment.export() and are not enumerated.
        """

        if not (self.valid and extract_audio):
            super().export(path)

        subprocess.run(
            "media/vgmstream/vgmstream",
            input=self.obj.read(),
            stdout=Path(path).with_suffix(".wav").open("wb"),
            stderr=subprocess.PIPE,
            check=True,
        )
