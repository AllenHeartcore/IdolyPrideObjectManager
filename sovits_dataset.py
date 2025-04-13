import shutil
import subprocess
import tempfile

from pathlib import Path
from argparse import ArgumentParser

from zipfile import ZipFile, ZipInfo
from datetime import datetime
from tqdm import tqdm

import GkmasObjectManager as gom
from GkmasObjectManager.log import Logger


logger = Logger()
logger.info("Fetching manifest...")
m = gom.fetch()


class CacheHandler:

    def __init__(self, cwd: Path, args=None):
        self.cwd = cwd
        self.args = args

        if self.cwd.exists():
            assert self.cwd.is_dir(), f"{self.cwd} is not a directory"
        else:
            self.cwd.mkdir(parents=True, exist_ok=True)

    def _rectify_filename(self, p: Path) -> str:
        return p.name

    def cache(self, target: list[str]):
        target = set(target)  # remove duplicates
        target -= set(map(self._rectify_filename, self.cwd.iterdir()))
        m.download(
            *sorted(list(target)),  # sort for logging
            path=self.cwd,
            categorize=False,
            convert_audio=True,
            audio_format="wav",  # avoid double compression
            unpack_subsongs=True,
        )

    def read(self, filename: str) -> bytes:
        return (self.cwd / filename).read_bytes()

    def read_multiple(self, filenames: list[str]) -> bytes:
        raise NotImplementedError("To be overridden in subclass")

    def purge(self):
        for f in tqdm(list(self.cwd.iterdir())):
            f.unlink()
        shutil.rmtree(self.cwd)


class SudCacheHandler(CacheHandler):

    def __init__(self, cwd: Path, args=None):
        super().__init__(cwd, args)

    def _rectify_filename(self, p: Path) -> str:
        f = p.name
        if f.startswith("sud_vo_adv_"):
            f = "_".join(f.split("_")[:-1])
        return Path(f).with_suffix(".acb").name

    def read(self, filename: str) -> bytes:
        return (
            (self.cwd / filename).read_bytes()
            if self.args.format == "wav"
            else subprocess.run(
                f"ffmpeg -i {self.cwd / filename} -f {self.args.format} -b:a {self.args.bitrate}k pipe:1",
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
            ).stdout
        )

    def read_multiple(self, filenames: list[str]) -> bytes:
        # SIDE EFFECT: Output directly written to args.output, as piped output can be corrupted
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as filelist:
            filelist.write(
                "".join([f"file '{self.cwd / f}'\n" for f in filenames]).encode()
            )
            filelist.flush()
        subprocess.run(
            f"ffmpeg -f concat -safe 0 -i {filelist.name} -f {self.args.format} -b:a {self.args.bitrate}k {self.args.output}",
            check=True,
        )
        Path(filelist.name).unlink()


if __name__ == "__main__":

    # ------------------------------ SETUP

    parser = ArgumentParser(
        description="Create a dataset for training a voice cloning model"
    )

    parser.add_argument("character", type=str, help="Character name")

    # output options
    parser.add_argument("-o", "--output", type=str, default="", help="Output filename")
    parser.add_argument("-f", "--format", type=str, default="wav", help="Output format")
    parser.add_argument("-b", "--bitrate", type=int, default=128, help="Output bitrate")
    parser.add_argument(
        "-m",
        "--merge",
        action="store_true",
        help="Merge dataset into one audio file (otherwise exported as ZIP)",
    )

    # caching options
    parser.add_argument(
        "-g", "--greedy", action="store_true", help="Search through all adventures"
    )
    parser.add_argument(
        "-c", "--cache-dir", type=str, default=".sovits-cache/", help="Cache directory"
    )
    parser.add_argument(
        "-p", "--purge-cache", action="store_true", help="Clear cache after use"
    )

    args = parser.parse_args()

    # ------------------------------ SANITY CHECKS

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
    if args.merge and args.output.suffix != f".{args.format}":
        ext = args.output.suffix[1:]
        logger.warning(
            f"Filename extension '{args.format}' does not match specified '{ext}', overriding"
        )
        args.output = args.output.with_suffix(f".{args.format}")

    assert not args.output.exists(), f"{args.output} already exists"
    if args.output.parent:
        args.output.parent.mkdir(parents=True, exist_ok=True)

    args.cache_dir = Path(args.cache_dir)
    sud_ch = SudCacheHandler(cwd=args.cache_dir, args=args)

    # ------------------------------ DOWNLOAD

    target = m.search(f"sud_vo.*{args.character}.*")
    if args.greedy:
        target += m.search(f"sud_vo_adv.*")
    target = set([f.name for f in target])  # remove duplicates

    if not target:
        logger.warning(f"Found no voice samples for '{args.character}, aborting")
        exit(1)
    logger.success(f"Found {len(target)} voice samples for '{args.character}'")

    logger.info("Caching samples...")
    sud_ch.cache(target)

    # ------------------------------ EXPORT

    logger.info("Filtering samples...")
    target_char = filter(
        lambda f: (
            args.character in f.name
            and not (
                f.name.startswith("sud_vo_adv_")
                and f.name.split("_")[-1].split("-")[0] != args.character
            )
            # exclude other characters in target character's personal story
        ),
        args.cache_dir.iterdir(),
    )

    logger.info("Exporting dataset...")
    if args.merge:
        sud_ch.read_multiple([f.name for f in target_char])
    else:
        with ZipFile(args.output, "w") as zipf:
            for f in tqdm(target_char):
                zipf.writestr(
                    ZipInfo(
                        f.with_suffix(f".{args.format}").name,
                        datetime.fromtimestamp(f.stat().st_mtime).timetuple(),
                    ),
                    sud_ch.read(f.name),
                )

    # ------------------------------ CLEANUP

    if args.purge_cache:
        logger.info("Purging cache...")
        sud_ch.purge()

    logger.success(f"Dataset ready at '{args.output}'")
