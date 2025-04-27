"""
media/audio.py
Unity audio conversion plugin for PrideAssetBundle,
and MP3 audio handler for PrideResource.
"""

from ..log import Logger
from .dummy import PrideDummyMedia

from io import BytesIO
from pathlib import Path

import UnityPy
from pydub import AudioSegment
from zipfile import ZipFile, ZipInfo
from datetime import datetime


logger = Logger()


class PrideAudio(PrideDummyMedia):
    """Handler for audio of common formats recognized by pydub."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.mimetype = "audio"
        self.raw_format = name.split(".")[-1][:-1]

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        audio = AudioSegment.from_file(BytesIO(raw))
        return audio.export(format=self.converted_format).read()


class PrideUnityAudio(PrideAudio):
    """Conversion plugin for Unity audio."""

    def __init__(self, name: str, raw: bytes, mtime: int):
        super().__init__(name, raw, mtime)
        self.raw_format = None  # don't override
        self.converted_format = "wav"

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)

        audioclips = [
            obj.read()
            for obj in (list(env.container.values()) + env.objects)
            if obj.type.name == "AudioClip"
        ]

        # Remove duplicates, since obj.samples will incur the largest overhead,
        # and we want to avoid running the decoding algorithm multiple times
        # if a clip appears in both env.container and env.objects;
        # Also this respects the order of env.container first.
        audioclips = {obj.name: obj for obj in audioclips}

        audio = {}
        for audioclip in audioclips.values():  # .samples comes with name already
            audio.update(audioclip.samples)  # yeah this 'samples' is a dict... bruh

        if not audio:
            raise ValueError("No AudioClip found in assetbundle")

        if self.converted_format != "wav":
            audio = {
                name: super()._convert(samples) for (name, samples) in audio.items()
            }

        if len(audio) == 1:
            return list(audio.values())[0]
            # discard clip name and follow assetbundle's filename

        with BytesIO() as buffer:
            with ZipFile(buffer, "w") as zip_file:
                dt = (
                    datetime.fromtimestamp(self.mtime) if self.mtime else datetime.now()
                )
                for name, samples in audio.items():
                    zip_file.writestr(
                        ZipInfo(
                            Path(name).with_suffix(f".{self.converted_format}").name,
                            date_time=dt.timetuple(),
                        ),
                        samples,
                    )
            return buffer.getvalue()
