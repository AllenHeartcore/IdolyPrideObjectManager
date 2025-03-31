import os
import shutil
import subprocess
from pathlib import Path
from argparse import ArgumentParser

import GkmasObjectManager as gom
from GkmasObjectManager.log import Logger


if __name__ == "__main__":

    logger = Logger()

    parser = ArgumentParser(
        description="Create a dataset for training a voice cloning model"
    )
    parser.add_argument("character", type=str, help="Character name")
    parser.add_argument("-o", "--output", type=str, default="", help="Output path")
    parser.add_argument("--format", type=str, default="wav", help="Output audio format")
    parser.add_argument("--tmpdir", type=str, default="tmp", help="Temporary directory")
    args = parser.parse_args()

    if args.output == "":
        args.output = f"sovits_dataset_{args.character}.{args.format}"

    if not args.output.endswith(args.format):
        ext = Path(args.output).suffix[1:]
        logger.warning(
            f"Filename extension '{args.format}' does not match specified '{ext}', overriding"
        )
        args.output = str(Path(args.output).with_suffix(f".{args.format}"))

    assert not os.path.exists(args.output), f"{args.output} already exists"
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if os.path.exists(args.tmpdir):
        assert os.path.isdir(args.tmpdir), f"{args.tmpdir} is not a directory"
        assert os.listdir(args.tmpdir) == [], f"{args.tmpdir} is not empty"
    else:
        os.makedirs(args.tmpdir)

    logger.info("Fetching manifest...")
    m = gom.fetch()

    logger.info(f"Downloading voice samples of '{args.character}'...")
    m.download(
        f"sud_vo.*{args.character}.*",
        path=args.tmpdir,
        categorize=False,
        convert_audio=True,
        audio_format=args.format,
        unpack_subsongs=True,
    )

    logger.info("Making dataset...")
    with open(os.path.join(args.tmpdir, "filelist.txt"), "w") as fout:
        for f in os.listdir(args.tmpdir):
            assert f.endswith(args.format)
            if (
                f.startswith("sud_vo_adv_")
                and f.split("_")[-1].split("-")[0] != args.character
            ):
                # exclude other characters in adventure voice pack
                # (hardcoded, can also set unpack_subsongs=False and check ZIP contents here)
                continue
            fout.write(f'file "{f}"\n')

    logger.info("Concatenating samples...")
    subprocess.run(
        f'ffmpeg -f concat -safe 0 -i {os.path.join(args.tmpdir, "filelist.txt")} -c copy -movflags +faststart "{args.output}"',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    logger.success(f"Dataset saved to {args.output}")
    logger.info("Cleaning up temporary files...")
    shutil.rmtree(args.tmpdir)
