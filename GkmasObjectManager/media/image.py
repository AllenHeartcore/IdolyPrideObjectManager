"""
media/image.py
Unity image conversion plugin for GkmasAssetBundle,
and PNG image handler for GkmasResource.
"""

from ..log import Logger
from ..const import IMAGE_RESIZE_ARGTYPE
from .dummy import GkmasDummyMedia
from .ai_caption import GPTImageCaptionEngine

from io import BytesIO
from pathlib import Path
from typing import Union, Tuple

import UnityPy
from PIL import Image


logger = Logger()


class GkmasImage(GkmasDummyMedia):
    """Handler for images of common formats recognized by PIL."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self._mimetype = "image"
        self._mimesubtype = name.split(".")[-1][:-1]
        self.converted = self.raw  # default to no reencoding

        # Assume we're working with **the same GkmasResource object**, called R, to handle a PNG.
        # We run the following sequence of operations:

        # - R.download()
        #   returns non-reencoded PNG bytes B1, since self.converted is initialized to self.raw.
        #       -   SIDE EFFECT: Children classes of GkmasImage will have to set self.converted to None to force reencoding.
        # - R._get_embed_url()
        #   returns base64-encoded B1 as PNG.

        # - R.download(image_format='JPEG')
        #   returns reencoded JPEG bytes B2 and update self.converted and self._mimesubtype.
        # - R._get_embed_url()
        #   returns base64-encoded B2 as JPEG, according to self._mimesubtype.

        # - R.download()
        #   returns JPEG bytes B2 this time since Dummy doesn't call _get_converted().
        #       -   IMPLICATIONS: kwargs.get("image_format", self._mimesubtype) == self._mimesubtype
        #           implies that no conversion is performed unless image_format is explicitly specified!
        # - R._get_embed_url()
        #   returns base64-encoded B2 as JPEG (unchanged)

        # - R.download(image_format='PNG')
        #   returns **reencoded** PNG bytes B3 and update self.converted and self._mimesubtype.
        # - R._get_embed_url()
        #   returns base64-encoded B3 as PNG, which is different from B1 since the image was JPEG-compressed once!
        #       -   The only way to get non-reencoded B1 at this point is to initialize a new GkmasResource object.

    def caption(self) -> str:
        return GPTImageCaptionEngine().generate(self._get_embed_url())

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        return self._img2bytes(Image.open(BytesIO(raw)), **kwargs)

    # don't put 'image_resize' in signature to match the parent class
    def _img2bytes(self, img: Image, **kwargs) -> bytes:
        """
        Args:
            image_resize (Union[None, str, Tuple[int, int]]) = None: Image resizing argument.
                If None, image is downloaded as is.
                If str, string must contain exactly one ':' and image is resized to the specified ratio.
                If Tuple[int, int], image is resized to the specified exact dimensions.
        """

        image_resize = kwargs.get("image_resize", None)
        if image_resize:
            if type(image_resize) == str:
                image_resize = self._determine_new_size(img.size, ratio=image_resize)
            img = img.resize(image_resize, Image.LANCZOS)

        io = BytesIO()
        try:
            img.save(io, format=self._mimesubtype.upper(), quality=100)
        except OSError:  # cannot write mode RGBA as {self._mimesubtype}
            img.convert("RGB").save(io, format=self._mimesubtype.upper(), quality=100)

        return io.getvalue()

    def _determine_new_size(
        self,
        size: Tuple[int, int],
        ratio: str,
        mode: Union["maximize", "ensure_fit", "preserve_npixel"] = "maximize",
    ) -> Tuple[int, int]:
        """
        [INTERNAL] Determines the new size of an image based on a given ratio.

        mode can be one of (terms borrowed from PowerPoint):
        - 'maximize': Enlarges the image to fit the ratio.
        - 'ensure_fit': Shrinks the image to fit the ratio.
        - 'preserve_npixel': Maintains approximately the same pixel count.

        Example: Given ratio = '4:3', an image of size (1920, 1080) is resized to:
        - (1920, 1440) in 'maximize' mode,
        - (1440, 1080) in 'ensure_fit' mode, and
        - (1663, 1247) in 'preserve_npixel' mode.
        """

        ratio = ratio.split(":")
        if len(ratio) != 2:
            raise ValueError("Invalid ratio format. Use 'width:height'.")

        ratio = (float(ratio[0]), float(ratio[1]))
        if ratio[0] <= 0 or ratio[1] <= 0:
            raise ValueError("Invalid ratio values. Must be positive.")

        ratio = ratio[0] / ratio[1]
        w, h = size
        ratio_old = w / h
        if ratio_old == ratio:
            return size

        w_new, h_new = w, h
        if mode == "preserve_npixel":
            pixel_count = w * h
            h_new = (pixel_count / ratio) ** 0.5
            w_new = h_new * ratio
        elif (mode == "maximize" and ratio_old > ratio) or (
            mode == "ensure_fit" and ratio_old < ratio
        ):
            h_new = w / ratio
        else:
            w_new = h * ratio

        round = lambda x: int(x + 0.5)  # round to the nearest integer
        return round(w_new), round(h_new)


class GkmasUnityImage(GkmasImage):
    """Conversion plugin for Unity images."""

    def __init__(self, name: str, raw: bytes):
        super().__init__(name, raw)
        self._mimetype = "image"
        self._mimesubtype = "png"
        self.converted = None  # don't inherit; Unity images are always reencoded

    def _convert(self, raw: bytes, **kwargs) -> bytes:
        env = UnityPy.load(raw)
        values = list(env.container.values())
        assert len(values) == 1, f"{self.name} contains {len(values)} images."
        return super()._img2bytes(values[0].read().image, **kwargs)
