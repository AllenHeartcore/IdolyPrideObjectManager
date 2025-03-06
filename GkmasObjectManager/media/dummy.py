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

        self._mimetype = None  # TO BE OVERRIDDEN
        self._mimesubtype = None  # TO BE OVERRIDDEN

    def _convert(self, raw: bytes) -> bytes:
        raise NotImplementedError  # TO BE OVERRIDDEN

    def _get_converted(self) -> bytes:
        if self.converted is None:
            self.converted = self._convert(self.raw)
        return self.converted

    def _get_embed_url(self) -> str:
        return f"data:{self._mimetype}/{self._mimesubtype};base64,{base64.b64encode(self._get_converted()).decode()}"

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
        path.with_suffix(f".{self._mimesubtype}").write_bytes(self._get_converted())
        logger.success(
            f"{self.name} downloaded and converted to {self._mimesubtype.upper()}"
        )
