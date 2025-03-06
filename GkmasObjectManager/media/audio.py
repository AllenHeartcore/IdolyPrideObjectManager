"""
media/audio.py
AWB/ACB audio conversion plugin for GkmasResource,
and MP3 audio handler for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

from pathlib import Path

import subprocess
from pydub import AudioSegment


logger = Logger()


class GkmasAudio(GkmasDummyMedia):
    """Handler for audio of common formats recognized by pydub."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self._mimetype = "audio"
        self._mimesubtype = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes) -> bytes:
        return raw


class GkmasAWBAudio(GkmasDummyMedia):
    """Conversion plugin for AWB audio."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self._mimetype = "audio"
        self._mimesubtype = "wav"

    def _convert(self, raw: bytes) -> bytes:

        audio = None
        success = False

        try:
            input_ext = self.name.split(".")[-1][:-1]
            Path(f"tmp.{input_ext}").write_bytes(raw)
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
            audio = AudioSegment.from_file("tmp.wav")
            success = True
        except Exception as e:
            pass  # handled by parent class
        finally:
            Path(f"tmp.{input_ext}").unlink(missing_ok=True)
            Path("tmp.wav").unlink(missing_ok=True)
            # this 'finally' block is why the 'success' flag,
            # along with all these try-catch hassle, ever exists

        if success:
            return audio.export(format="wav").read()
        else:
            raise e  # delay the exception after cleanup
