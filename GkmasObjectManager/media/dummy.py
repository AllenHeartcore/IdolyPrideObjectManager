"""
media/dummy.py
Dummy media conversion plugin.
Serves as a base class & template for other media plugins,
as well as a fallback for unknown media types.
"""

from ..log import Logger

import base64
from pathlib import Path


logger = Logger()


class GkmasDummyMedia:
    """Unrecognized media handler, also the fallback for conversion plugins."""

    def __init__(self, name: str, raw: bytes):
        self.name = name  # only for logging
        self.raw = raw  # raw binary data (we don't want to reencode known formats)
        self.converted = None  # converted binary data (if applicable)

        self.mimetype = None  # TO BE OVERRIDDEN ('image', 'audio', 'video', etc.)
        self.raw_format = None  # TO BE OVERRIDDEN
        self.converted_format = None  # TO BE OVERRIDDEN

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        return raw  # TO BE OVERRIDDEN
        # a NotImplementedError would propagate to the frontend;
        # instead, we return a clean bytestream for download

    def _get_data(self, **kwargs) -> bytes:

        fmt = kwargs.get(
            f"{self.mimetype}_format",
            self.raw_format or self.converted_format,  # fallback if _raw_format is None
        )
        if self.raw_format == fmt:  # rawdump
            return self.raw

        if self.converted_format != fmt:
            self.converted_format = fmt  # maintain consistency
            self.converted = None

        if self.converted is None:
            self.converted = self._convert(self.raw, **kwargs)
            # child classes don't need to put '..._format' in signature of _convert()
            # since it has already been synchronized into self.converted_format

        return self.converted

    def _get_embed_url(self, **kwargs) -> str:
        converted = self._get_data(**kwargs)  # may overwrite self.converted_format
        return f"data:{self.mimetype}/{self.converted_format};base64,{base64.b64encode(converted).decode()}"

    def caption(self) -> str:
        return "[Captioning not supported for this data type.]"

    def export(self, path: Path, **kwargs):
        if kwargs.get(f"convert_{self.mimetype}", True):
            try:
                self._export_converted(path, **kwargs)
            except:
                logger.warning(f"{self.name} failed to convert, fallback to rawdump")
                self._export_raw(path)
        else:
            self._export_raw(path)

    def _export_raw(self, path: Path):
        path.write_bytes(self.raw)
        logger.success(f"{self.name} downloaded")

    def _export_converted(self, path: Path, **kwargs):
        converted = self._get_data(**kwargs)  # may overwrite self.converted_format
        path.with_suffix(f".{self.converted_format}").write_bytes(converted)
        logger.success(
            f"{self.name} downloaded and converted to {self.converted_format.upper()}"
        )
