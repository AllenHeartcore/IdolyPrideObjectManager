from pathlib import Path
from sys import argv

cat_instrs = [
    ("story-thumb", lambda s: s.split("_")[3]),
]


if __name__ == "__main__":

    root = argv[1]

    for subdir, cat_func in cat_instrs:
        parent = Path(root, subdir)

        for f in parent.iterdir():
            cat = cat_func(f.name)
            (parent / cat).mkdir(parents=True, exist_ok=True)
            f.rename(parent / cat / f.name)
