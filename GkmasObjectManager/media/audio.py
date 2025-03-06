"""
media/audio.py
AWB/ACB audio conversion plugin for GkmasResource,
and MP3 audio handler for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

from pathlib import Path

import os
import tempfile
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
            tmp_in = tempfile.NamedTemporaryFile(suffix=f".{input_ext}", delete=False)
            tmp_in.write(raw)
            tmp_out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            process = subprocess.run(
                [
                    Path(__file__).parent / "vgmstream/vgmstream",
                    "-o",
                    tmp_out.name,
                    tmp_in.name,
                ],
                shell=True,  # Otherwise, gets [WinError 193] 'invalid Win32 application'
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,  # suppresses console output
            )
            assert process.returncode == 0
            audio = AudioSegment.from_file(tmp_out.name)
            success = True
        except Exception as e:
            exception = e  # 'e' only lives in the 'except' block
            # parent class handles the rest
        finally:
            tmp_in.close()
            tmp_out.close()
            os.remove(tmp_in.name)
            os.remove(tmp_out.name)
            # this 'finally' block is why the 'success' flag,
            # along with all these try-catch hassle, ever exists
            # (vgmstream doesn't like NamedTemporaryFile with delete=True)

        if success:
            return audio.export(format="wav").read()
        else:
            raise exception  # delay the exception after cleanup
