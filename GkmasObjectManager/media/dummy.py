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

        self._mimetype = None  # TO BE OVERRIDDEN ('image', 'audio', 'video', etc.)
        self._mimesubtype = None  # TO BE OVERRIDDEN (desired format for self.converted)
        self._raw_format = None  # TO BE OVERRIDDEN
        # self._mimesubtype is the **desired** format for self.converted,
        #   and may be overwritten by _get_converted() if the format is specified in kwargs.
        # self._raw_format is the **inherent** format of self.raw,
        #   is used to determine if rawdump is necessary, and is never overwritten.

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        return raw  # TO BE OVERRIDDEN
        # a NotImplementedError would propagate to the frontend;
        # instead, we return a clean bytestream for download

    def _get_converted(self, **kwargs) -> bytes:

        fmt = kwargs.get(
            f"{self._mimetype}_format",
            self._raw_format or self._mimesubtype,  # fallback if _raw_format is None
        )
        if self._raw_format == fmt:  # rawdump
            return self.raw

        if self._mimesubtype != fmt:
            self._mimesubtype = fmt  # maintain consistency
            self.converted = None

        if self.converted is None:
            self.converted = self._convert(self.raw, **kwargs)
            # child classes don't need to put '..._format' in signature of _convert()
            # since it has already been synchronized into self._mimesubtype

        return self.converted

    def _get_embed_url(self, **kwargs) -> str:
        converted = self._get_converted(**kwargs)  # may overwrite self._mimesubtype
        return f"data:{self._mimetype}/{self._mimesubtype};base64,{base64.b64encode(converted).decode()}"

    def caption(self) -> str:
        return "[Captioning not supported for this data type.]"

    def export(self, path: Path, **kwargs):
        if kwargs.get(f"convert_{self._mimetype}", True):
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
        converted = self._get_converted(**kwargs)  # may overwrite self._mimesubtype
        path.with_suffix(f".{self._mimesubtype}").write_bytes(converted)
        logger.success(
            f"{self.name} downloaded and converted to {self._mimesubtype.upper()}"
        )
