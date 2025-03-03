"""
media/image.py
Unity image extraction plugin for GkmasAssetBundle.
"""

from ..log import Logger
from ..const import IMG_RESIZE_ARGTYPE

import UnityPy
from pathlib import Path
from typing import Union, Tuple
from PIL import Image


logger = Logger()


class GkmasUnityImage:

    def __init__(
        self,
        name: str,
        data: bytes,
    ):
        """
        Initializes **one** Unity image from raw assetbundle bytes.
        Raises a warning and falls back to raw dump if the bundle contains multiple objects.
        """

        self.valid = True
        self.name = name

        env = UnityPy.load(data)
        values = list(env.container.values())

        if len(values) != 1:
            logger.warning(f"{name} contains {len(values)} images, fallback to rawdump")
            self.valid = False
            return  # fallback case is handled within this class

        self.img = values[0].read().image

    def export(
        self,
        path: Path,
        img_format: str,
        img_resize: IMG_RESIZE_ARGTYPE,
    ):
        """
        Attempts to extract a single image from the assetbundle's container.
        """

        if not self.valid:
            path.write_bytes(self.img)
            logger.success(f"{self.name} downloaded")
            return

        img = self.img

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
