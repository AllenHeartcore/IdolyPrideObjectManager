import os
from sys import argv


cat_instrs = [
    ("produce/skillcard", lambda s: s.split("_")[-2]),
]


if __name__ == "__main__":

    root = argv[1]

    for subdir, cat_func in cat_instrs:
        parent = os.path.join(root, subdir)

        for f in os.listdir(parent):
            cat = cat_func(f)
            os.makedirs(os.path.join(parent, cat), exist_ok=True)
            os.rename(os.path.join(parent, f), os.path.join(parent, cat, f))
