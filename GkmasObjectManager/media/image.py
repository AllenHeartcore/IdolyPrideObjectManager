"""
media/image.py
Unity image extraction plugin for GkmasAssetBundle.
"""

from ..log import Logger
from ..const import IMG_RESIZE_ARGTYPE
from .dummy import GkmasDummyMedia
from .ai_caption import GPTImageCaptionEngine

import base64
import UnityPy
from io import BytesIO
from pathlib import Path
from typing import Union, Tuple
from PIL import Image


logger = Logger()


class GkmasUnityImage(GkmasDummyMedia):

    def __init__(
        self,
        name: str,
        data: bytes,
    ):
        """
        Initializes **one** Unity image from raw assetbundle bytes.
        Raises a warning and falls back to raw dump if the bundle contains multiple objects.
        """

        super().__init__(name, data)

        env = UnityPy.load(data)
        values = list(env.container.values())

        if len(values) != 1:
            logger.warning(f"{name} contains {len(values)} images, fallback to rawdump")
            self.valid = False
            return  # fallback case is handled within this class

        self.obj = values[0].read().image

    def _get_embed_url(self) -> str:
        io = BytesIO()
        self.obj.save(io, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(io.getvalue()).decode()}"

    def caption(self) -> str:
        return GPTImageCaptionEngine().generate(self._get_embed_url())

    def export(
        self,
        path: Path,
        extract_img: bool = True,
        img_format: str = "png",
        img_resize: IMG_RESIZE_ARGTYPE = None,
    ):
        """
        Attempts to extract a single image from the assetbundle's container.

        Args:
            extract_img (bool) = True: Whether to extract a single image from assetbundles of type 'img'.
                If False, 'img_.*\\.unity3d' is downloaded as is.
            img_format (str) = 'png': Image format for extraction. Case-insensitive.
                Effective only when 'extract_img' is True.
                Valid options are checked by PIL.Image.save() and are not enumerated.
            img_resize (Union[None, str, Tuple[int, int]]) = None: Image resizing argument.
                If None, image is downloaded as is.
                If str, string must contain exactly one ':' and image is resized to the specified ratio.
                If Tuple[int, int], image is resized to the specified exact dimensions.
        """

        if not (self.valid and extract_img):
            super().export(path)

        img = self.obj

        if img_resize:
            if type(img_resize) == str:
                img_resize = self._determine_new_size(img.size, ratio=img_resize)
            img = img.resize(img_resize, Image.LANCZOS)

        try:
            img.save(path.with_suffix(f".{img_format.lower()}"), quality=100)
        except OSError:  # cannot write mode RGBA as {img_format}
            img = img.convert("RGB")
            img.save(path.with_suffix(f".{img_format.lower()}"), quality=100)

        logger.success(f"{self.name} downloaded and extracted as {img_format.upper()}")

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
