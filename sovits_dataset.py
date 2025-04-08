import shutil
import subprocess
from pathlib import Path
from argparse import ArgumentParser
from zipfile import ZipFile
from tqdm import tqdm

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
    parser.add_argument("-f", "--format", type=str, default="mp3", help="Output format")
    parser.add_argument("-b", "--bitrate", type=int, default=128, help="Output bitrate")

    parser.add_argument(
        "-g", "--greedy", action="store_true", help="Search through all adventures"
    )
    parser.add_argument(
        "-m",
        "--merge",
        action="store_true",
        help="Merge dataset into one audio file (otherwise exported as ZIP)",
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
        args.output = "".join(
            [
                f"sovits_dataset_v{m.revision._get_canon_repr()}",
                f"_{args.character}",
                "_greedy" if args.greedy else "",
                f".{args.format}" if args.merge else ".zip",
            ]
        )

    args.output = Path(args.output)
    if args.merge and not args.output.suffix == f".{args.format}":
        ext = args.output.suffix[1:]
        logger.warning(
            f"Filename extension '{args.format}' does not match specified '{ext}', overriding"
        )
        args.output = args.output.with_suffix(f".{args.format}")

    assert not args.output.exists(), f"{args.output} already exists"
    if args.output.parent:
        args.output.parent.mkdir(parents=True, exist_ok=True)

    args.cache_dir = Path(args.cache_dir)
    cache_active = False
    if args.cache_dir.exists():
        assert args.cache_dir.is_dir(), f"{args.cache_dir} is not a directory"
        if list(args.cache_dir.iterdir()):
            cache_active = True
    else:
        args.cache_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------ DOWNLOAD

    target = m.search(f"sud_vo.*{args.character}.*")
    if args.greedy:
        target += m.search(f"sud_vo_adv.*")
    target = set([f.name for f in target])  # remove duplicates
    if not target:
        logger.warning(f"Found no voice samples for '{args.character}, aborting")
        exit(1)
    logger.success(f"Found {len(target)} voice samples for '{args.character}'")

    if cache_active:
        logger.info("Computing cache diff...")
        cached_names = [f.name for f in args.cache_dir.iterdir()]
        target -= set(
            [
                Path("_".join(f.split("_")[:-1]) if f.startswith("sud_vo_adv_") else f)
                .with_suffix(".acb")
                .name
                for f in cached_names
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

    # ------------------------------ EXPORT

    logger.info("Filtering samples...")
    target_char = [
        f
        for f in args.cache_dir.iterdir()
        if (
            f != "filelist.txt"
            and args.character in f.name
            and not (
                f.name.startswith("sud_vo_adv_")
                and f.name.split("_")[-1].split("-")[0] != args.character
            )
            # exclude other characters in adventure voice pack
            # (hardcoded, can also set unpack_subsongs=False and check ZIP contents here)
        )
    ]

    logger.info("Exporting dataset...")
    if args.merge:
        filelist_path = Path(args.cache_dir, "filelist.txt")
        filelist_path.write_text(
            "".join([f"file '{f.name.replace("\\", "/")}'\n" for f in target_char])
        )
        subprocess.run(
            f'ffmpeg -f concat -safe 0 -i {filelist_path} -b:a {args.bitrate}k "{args.output}"',
            check=True,
        )
        filelist_path.unlink()
    else:
        with ZipFile(args.output, "w") as zipf:
            for f in tqdm(target_char):
                proc = subprocess.run(
                    f"ffmpeg -i {f} -f {args.format} -b:a {args.bitrate}k pipe:1",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )
                zipf.writestr(Path(f).with_suffix(f".{args.format}").name, proc.stdout)

    # ------------------------------ CLEANUP

    if not (cache_active or args.keep_cache):
        logger.info("Purging cache...")
        shutil.rmtree(args.cache_dir)

    logger.success(f"Dataset ready at '{args.output}'")
