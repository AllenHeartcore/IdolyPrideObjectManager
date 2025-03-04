import os
from sys import argv

import GkmasObjectManager as gom


instructions_dl = [
    (r"img_general_cidol.*thumb-landscape-large.*", "cidol-landscape", "16:9", "jpg"),
    (r"img_general_cidol.*full.*", "cidol-portrait", "9:16", "jpg"),
    (r"img_general_csprt.*full.*", "csprt", "16:9", "jpg"),
    (r"img_general_meishi_base_story-bg.*full.*", "bg", "16:9", "jpg"),
    (r"img_general_meishi_base_(?!story-bg).*full.*", "base", "16:9", "png"),
]

if __name__ == "__main__":

    assert len(argv) == 2, "Usage: python make_wallpaper_kit.py <manifest>"

    manifest = gom.load(argv[1])
    target = f"gkmas_wallpaper_kit_v{manifest.revision._get_canon_repr()}/"

    for pattern, subdir, ratio, fmt in instructions_dl:

        manifest.download(
            pattern,
            path=target + subdir,
            categorize=False,
            img_format=fmt,
            img_resize=ratio,
        )
