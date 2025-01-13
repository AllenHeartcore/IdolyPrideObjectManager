import os
from sys import argv

import GkmasObjectManager as gom
from GkmasObjectManager.const import CHARACTER_ABBREVS
from GkmasObjectManager.log import Logger


instructions_dl = [
    (r"img_general_icon_contest-rank.*", "profile"),
    (r"img_general_meishi_illust_idol.*", "idol/full"),
    (r"img_general_meishi_illust_sd.*", "idol/mini", "2:3"),
    (r"img_general_cidol.*full\..*", "idol/produce", "9:16", "jpg"),
    (r"img_general_cidol.*thumb-landscape-large.*", "idol/produce", "16:9", "jpg"),
    (r"img_general_cidol.*thumb-portrait.*", "idol/produce", "3:4"),
    (r"img_general_meishi_illust_sign.*", "idol/sign"),
    (r"img_general_csprt.*full\..*", "support", "16:9", "jpg"),
    (r"img_general_meishi_base_story-bg.*", "base/commu", "16:9", "jpg"),
    (r"img_general_meishi_base_(?!story-bg).*full\..*", "base", "16:9", "jpg"),
    (r"img_general_achievement_produce.*", "achievement/produce"),
    (r"img_general_achievement_common.*", "achievement/misc"),
    (r"img_general_meishi_illust_music-logo.*", "parts/logo", "3:2"),
    (r"img_general_meishi_illust_pict-icon.*", "parts/icon"),
    (r"img_general_meishi_illust_stamp.*", "parts/misc"),
    (r"img_general_meishi_illust_hatsuboshi-logo.*", "parts/misc"),
    (r"img_general_meishi_illust_event.*", "parts/event"),  # Inferred
    (r"img_general_meishi_illust_highscore.*full\..*", "parts/highscore"),  # Inferred
    (r"img_general_skillcard.*", "produce/skillcard"),
    (r"img_general_pitem.*", "produce/pitem"),
    (r"img_general_pdrink.*", "produce/pdrink"),
]

# Have to hardcode the number 10, otherwise this requires empty folder post-detection
for char in CHARACTER_ABBREVS[:10]:
    instructions_dl.extend(
        [
            (f"img_general_achievement_{char}.*", f"achievement/idol/{char}"),
            (f"img_general_achievement_char_{char}.*", f"achievement/idol/{char}"),
        ]
    )

# These situations are not common enough to be generalized in the module
instructions_pack = [
    ("idol/produce", lambda s: s.split("_")[-2].split("-")[1]),
    ("produce/skillcard", lambda s: s.split("_")[-2]),
]


if __name__ == "__main__":

    assert len(argv) == 2, "Usage: python make_namecard_kit.py <manifest>"
    logger = Logger()

    manifest = gom.load(argv[1])
    target = f"gkmas_namecard_kit_{manifest.revision}/"  # output directory

    for pattern, subdir, *config in instructions_dl:
        logger.info(f"Populating '{subdir}'")

        ratio = config[0] if config else None
        fmt = config[1] if len(config) > 1 else "png"
        # In this case, all JPGs must be resized, but this remains unfixed
        # since this instruction-based coding style can hardly be generalized

        manifest.download(
            pattern,
            path=target + subdir,
            categorize=False,
            extract_img=True,
            img_format=fmt,
            img_resize=ratio,
        )

    for subdir, cat_func in instructions_pack:
        logger.info(f"Post-categorizing '{subdir}'")
        parent = target + subdir
        for f in os.listdir(parent):
            cat = cat_func(f)
            os.makedirs(os.path.join(parent, cat), exist_ok=True)
            os.rename(os.path.join(parent, f), os.path.join(parent, cat, f))

    logger.info(f"Namecard kit ready at '{target}'")
