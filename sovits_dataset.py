import re
import json
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
from GkmasObjectManager.object import GkmasResource


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

    def cache(self, target: list[GkmasResource]):
        target = set([t.name for t in target])  # remove duplicates
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
        # TO BE OVERRIDDEN IN SUBCLASS
        return (self.cwd / filename).read_bytes()

    def export_multiple(self, filenames: list[str], path: Path = None):
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

    def export_multiple(self, filenames: list[str], path: Path = None):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as filelist:
            filelist.write(
                "".join([f"file '{self.cwd / f}'\n" for f in filenames]).encode()
            )
            filelist.flush()
        subprocess.run(
            f"ffmpeg -f concat -safe 0 -i {filelist.name} -f {self.args.format} -b:a {self.args.bitrate}k {path or self.args.output}",
            check=True,
        )
        Path(filelist.name).unlink()


class AdvCacheHandler(CacheHandler):

    def __init__(self, cwd: Path, args=None):
        super().__init__(cwd, args)
        self._caption_map = {}
        self._caption_map_ready = False

    def _rectify_filename(self, p: Path) -> str:
        return p.with_suffix(".txt").name

    def _update_caption_map(self, commands):
        commands = sorted(
            filter(lambda cmd: cmd["cmd"] in ["message", "voice"], commands),
            key=lambda cmd: cmd["clip"]["_startTime"],
        )  # m- and v- commands don't necessarily go together in raw data
        for cmd1, cmd2 in zip(commands, commands[1:]):
            if cmd1["cmd"] == "voice" and cmd2["cmd"] == "message":
                self._caption_map[cmd1["voice"]] = cmd2["text"]
            elif cmd1["cmd"] == "message" and cmd2["cmd"] == "voice":
                self._caption_map[cmd2["voice"]] = cmd1["text"]

    def _build_caption_map(self):
        if self._caption_map_ready:
            return
        for f in tqdm(self.cwd.iterdir()):
            assert f.suffix == ".json", f"Non-JSON file cached in {self.cwd}"
            self._update_caption_map(json.loads(f.read_text(encoding="utf-8")))
        self._caption_map_ready = True

    def cache(self, target: list[GkmasResource]):
        # this can be inefficient; but building _caption_map
        # on the fly requires real-time access to resource._media,
        # whose interface is wrapped in the download() dispatcher
        self._caption_map_ready = False
        super().cache(target)

    # By returning str instead of bytes, we can avoid double encoding
    # but have also broken inheritance consistency with CacheHandler
    def read(self, filename: str) -> str:
        self._build_caption_map()
        caption = self._caption_map.get(filename.split(".")[0], "")
        # this is a bit insecure since it assumes no dot in filename,
        # but converting to Path here creates additional overhead
        return re.escape(caption)

    def read_multiple(self, filenames: list[str]) -> str:
        captions = [self.read(f) for f in filenames]
        if self.args.merge:
            return "\n".join(captions)
        else:
            return "".join([f"{f},{c}\n" for f, c in zip(filenames, captions)])

    def export_multiple(self, filenames: list[str], path: Path = None):
        path = path or self.args.output.with_suffix(".txt")
        path.write_text(self.read_multiple(filenames), encoding="utf-8")


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
    parser.add_argument("-c", "--caption", action="store_true", help="Include captions")
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
        "-d", "--cache-dir", type=str, default=".sovits-cache/", help="Cache directory"
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

    args.cache_dir = Path(args.cache_dir).resolve()  # record absolute path in filelist
    sud_ch = SudCacheHandler(cwd=args.cache_dir / "sud", args=args)
    if args.caption:
        adv_ch = AdvCacheHandler(cwd=args.cache_dir / "adv", args=args)

    # ------------------------------ DOWNLOAD

    target_sud = m.search(f"sud_vo_adv.*{'' if args.greedy else args.character}.*")
    if not args.caption:
        target_sud += m.search(f"sud_vo.*{args.character}.*")
        # 'general' and 'system' voice samples don't have captions

    if not target_sud:
        logger.warning(f"Found no voice samples for '{args.character}', aborting")
        exit(1)
    logger.success(f"Found {len(target_sud)} voice samples for '{args.character}'")

    if args.caption:
        target_adv = m.search(f"adv.*{'' if args.greedy else args.character}.*")

    logger.info("Caching samples...")
    sud_ch.cache(target_sud)
    if args.caption:
        adv_ch.cache(target_adv)

    # ------------------------------ EXPORT

    logger.info("Filtering samples...")
    target_export = list(
        filter(
            lambda f: (
                args.character in f.name
                and not (
                    f.name.startswith("sud_vo_adv_")
                    and f.name.split("_")[-1].split("-")[0] != args.character
                )
                # exclude other characters in target character's personal story
            ),
            sud_ch.cwd.iterdir(),
        )
    )  # convert to list to avoid generator expression issues

    logger.info("Exporting dataset...")
    if args.merge:
        sud_ch.export_multiple([f.name for f in target_export])
        adv_ch.export_multiple([f.name for f in target_export])
    else:
        with ZipFile(args.output, "w") as zipf:
            zipf.writestr(
                ZipInfo("captions.txt"),
                adv_ch.read_multiple([f.name for f in target_export]),
            )
            for f in tqdm(target_export):
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
