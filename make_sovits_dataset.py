import os
import shutil
import subprocess
from pathlib import Path
from argparse import ArgumentParser

import GkmasObjectManager as gom
from GkmasObjectManager.log import Logger


if __name__ == "__main__":

    # ------------------------------ SETUP

    logger = Logger()

    parser = ArgumentParser(
        description="Create a dataset for training a voice cloning model"
    )

    parser.add_argument("character", type=str, help="Character name")

    parser.add_argument("-o", "--output", type=str, default="", help="Output filename")
    parser.add_argument("-f", "--format", type=str, default="wav", help="Output format")
    parser.add_argument("-b", "--bitrate", type=int, default=128, help="Output bitrate")

    parser.add_argument(
        "-g", "--greedy", action="store_true", help="Search through all adventures"
    )
    parser.add_argument(
        "-c", "--cache-dir", type=str, default=".sovits-cache/", help="Cache directory"
    )
    parser.add_argument(
        "-k", "--keep-cache", action="store_true", help="Skip cache cleanup"
    )

    args = parser.parse_args()

    # ------------------------------ SANITY CHECKS

    logger.info("Fetching manifest...")
    m = gom.fetch()

    if args.output == "":
        args.output = f"sovits_dataset_v{m.revision._get_canon_repr()}_{args.character}{"_greedy" if args.greedy else ""}.{args.format}"

    if not args.output.endswith(args.format):
        ext = Path(args.output).suffix[1:]
        logger.warning(
            f"Filename extension '{args.format}' does not match specified '{ext}', overriding"
        )
        args.output = str(Path(args.output).with_suffix(f".{args.format}"))

    assert not os.path.exists(args.output), f"{args.output} already exists"
    if os.path.dirname(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

    cache_active = False
    if os.path.exists(args.cache_dir):
        assert os.path.isdir(args.cache_dir), f"{args.cache_dir} is not a directory"
        if os.listdir(args.cache_dir):
            cache_active = True
    else:
        os.makedirs(args.cache_dir)

    # ------------------------------ CORE

    target = m.search(f"sud_vo.*{args.character}.*")
    if args.greedy:
        target += m.search(f"sud_vo_adv.*")
    target = set([f.name for f in target])
    if not target:
        logger.warning(f"Found no voice samples for '{args.character}, aborting")
        exit(1)
    logger.success(f"Found {len(target)} voice samples for '{args.character}'")

    if cache_active:
        logger.info("Computing cache diff...")
        target -= set(
            [
                str(
                    Path(
                        "_".join(f.split("_")[:-1])
                        if f.startswith("sud_vo_adv_")
                        else f
                    ).with_suffix(".acb")
                )
                for f in os.listdir(args.cache_dir)
            ]
        )

    logger.info(f"Downloading samples...")
    m.download(
        *sorted(list(target)),  # sort for logging
        path=args.cache_dir,
        categorize=False,
        convert_audio=True,
        audio_format="wav",  # avoid double compression
        unpack_subsongs=True,
    )

    logger.info("Making dataset...")
    with open(os.path.join(args.cache_dir, "filelist.txt"), "w") as fout:
        for f in os.listdir(args.cache_dir):

            if (
                f == "filelist.txt"
                or args.character not in f
                or (
                    f.startswith("sud_vo_adv_")
                    and f.split("_")[-1].split("-")[0] != args.character
                )
            ):
                continue
                # exclude other characters in adventure voice pack
                # (hardcoded, can also set unpack_subsongs=False and check ZIP contents here)

            fout.write(f"file '{f}'\n")

    logger.info("Concatenating samples...")
    subprocess.run(
        f'ffmpeg -f concat -safe 0 -i {os.path.join(args.cache_dir, "filelist.txt")} -b:a {args.bitrate}k "{args.output}"',
        check=True,
    )

    os.remove(os.path.join(args.cache_dir, "filelist.txt"))
    if not (cache_active or args.keep_cache):
        logger.info("Purging cache...")
        shutil.rmtree(args.cache_dir)

    logger.success(f"Dataset ready at '{args.output}'")
