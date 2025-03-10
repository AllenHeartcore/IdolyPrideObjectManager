"""
media/audio.py
AWB/ACB audio conversion plugin for GkmasResource,
and MP3 audio handler for GkmasResource.
"""

from ..log import Logger
from .dummy import GkmasDummyMedia

import os
import platform
import tempfile
import subprocess
from io import BytesIO
from pathlib import Path

import UnityPy
from pydub import AudioSegment


logger = Logger()


class GkmasAudio(GkmasDummyMedia):
    """Handler for audio of common formats recognized by pydub."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.mimetype = "audio"
        self.raw_format = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        audio = AudioSegment.from_file(BytesIO(raw))
        return audio.export(format=self.converted_format).read()


class GkmasUnityAudio(GkmasAudio):
    """Conversion plugin for Unity audio."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.raw_format = None  # don't override
        self.converted_format = "wav"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        assert len(values) == 1, f"{self.name} contains {len(values)} audio clips."
        samples = values[0].read().samples
        sample = list(samples.values())[0]
        return sample if self.converted_format == "wav" else super()._convert(sample)
        # UnityPy is decompressing AudioClip into clean PCM bytes for us


class GkmasAWBAudio(GkmasDummyMedia):
    """Conversion plugin for AWB audio."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self.mimetype = "audio"
        self.converted_format = "wav"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        # doesn't use pydub, which is why this class is not inherited from GkmasAudio

        audio = None
        success = False

        try:
            input_ext = self.name.split(".")[-1][:-1]
            tmp_in = tempfile.NamedTemporaryFile(suffix=f".{input_ext}", delete=False)
            tmp_in.write(raw)
            tmp_out = tempfile.NamedTemporaryFile(
                suffix=f".{self.converted_format}", delete=False
            )

            system_name = platform.system()
            if system_name == "Windows":
                exe_suffix = "win"
            elif system_name == "Linux":
                exe_suffix = "linux"
            elif system_name == "Darwin":
                exe_suffix = "mac"
            else:
                raise OSError(f"Unsupported system: {system_name}")

            process = subprocess.run(
                [
                    Path(__file__).parent / f"vgmstream/vgmstream-{exe_suffix}",
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
            return audio.export(format=self.converted_format).read()
        else:
            raise exception  # delay the exception after cleanup
