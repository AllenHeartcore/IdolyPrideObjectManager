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

        try:
            input_ext = name.split(".")[-1][:-1]
            Path(f"tmp.{input_ext}").write_bytes(data)
            process = subprocess.run(
                [
                    Path(__file__).parent / "vgmstream/vgmstream",
                    "-o",
                    "tmp.wav",
                    f"tmp.{input_ext}",
                ],
                shell=True,  # Otherwise, gets [WinError 193] 'invalid Win32 application'
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,  # suppresses console output
            )
            assert process.returncode == 0
            self.obj = AudioSegment.from_file("tmp.wav")
        except:
            logger.warning(
                f"{name} is not recognized by vgmstream, fallback to rawdump"
            )
            # fallback case is handled within this class
            self.valid = False
        finally:
            Path(f"tmp.{input_ext}").unlink(missing_ok=True)
            Path("tmp.wav").unlink(missing_ok=True)

    def _get_embed_url(self) -> str:
        if not self.valid:
            return super()._get_embed_url()
        buffer = BytesIO()
        self.obj.export(buffer, format="wav")
        buffer.seek(0)
        return f"data:audio/wav;base64,{base64.b64encode(buffer.getvalue()).decode()}"

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

        self.obj.export(path.with_suffix(f".{audio_format}"), format=audio_format)
        logger.success(
            f"{self.name} downloaded and extracted as {audio_format.upper()}"
        )
