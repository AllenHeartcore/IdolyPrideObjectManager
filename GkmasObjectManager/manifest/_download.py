"""
_download.py
[CLASS SPLIT] GkmasManifest-managed object downloading.
"""

from .utils import ConcurrentDownloader
from ..const import (
    ALL_ASSETBUNDLES,
    ALL_RESOURCES,
    PATH_ARGTYPE,
    IMG_RESIZE_ARGTYPE,
    DEFAULT_DOWNLOAD_PATH,
    DEFAULT_DOWNLOAD_NWORKER,
)

import re


def download(
    self,
    *criteria: str,
    nworker: int = DEFAULT_DOWNLOAD_NWORKER,
    path: PATH_ARGTYPE = DEFAULT_DOWNLOAD_PATH,
    categorize: bool = True,
    extract_img: bool = True,
    img_format: str = "png",
    img_resize: IMG_RESIZE_ARGTYPE = None,
):
    """
    Downloads the regex-specified assetbundles/resources to the specified path.

    Args:
        *criteria (str): Regex patterns of assetbundle/resource names.
            Allowed special tokens are const.ALL_ASSETBUNDLES and const.ALL_RESOURCES.
        nworker (int) = DEFAULT_DOWNLOAD_NWORKER: Number of concurrent download workers.
            Defaults to multiprocessing.cpu_count().
        path (Union[str, Path]) = DEFAULT_DOWNLOAD_PATH: A directory to which the objects are downloaded.
            *WARNING: Behavior is undefined if the path points to an definite file (with extension).*
        categorize (bool) = True: Whether to categorize the downloaded objects into subdirectories.
            If False, all objects are downloaded to the specified 'path' in a flat structure.
        extract_img (bool) = True: Whether to extract images from assetbundles of type 'img'.
            If False, 'img_.*\\.unity3d' are downloaded as is.
        img_format (str) = 'png': Image format for extraction. Case-insensitive.
            Effective only when 'extract_img' is True. Format must support RGBA mode.
            Valid options are checked by PIL.Image.save() and are not enumerated.
        img_resize (Union[None, str, Tuple[int, int]]) = None: Image resizing argument.
            If None, images are downloaded as is.
            If str, string must contain exactly one ':' and images are resized to the specified ratio.
            If Tuple[int, int], images are resized to the specified exact dimensions.
    """

    objects = []

    for criterion in criteria:
        if criterion == ALL_ASSETBUNDLES:  # special tokens, enclosed in <>
            objects.extend(self.abs)
        elif criterion == ALL_RESOURCES:
            objects.extend(self.reses)
        else:
            objects.extend(
                [
                    self._name2object[file]
                    for file in self._name2object
                    if re.match(criterion, file)
                ]
            )

    ConcurrentDownloader(nworker).dispatch(
        objects,
        path=path,
        categorize=categorize,
        extract_img=extract_img,
        img_format=img_format,
        img_resize=img_resize,
    )
