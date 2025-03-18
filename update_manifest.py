"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import GkmasObjectManager as gom

import os
import sys
from pathlib import Path


def do_update(dir: str, pc: bool = False) -> bool:

    m_remote = gom.fetch(pc=pc)
    rev_remote = m_remote.revision._get_canon_repr()
    rev_local = int((Path(dir) / "LATEST_REVISION").read_text())

    if rev_remote == rev_local:
        print("No update available.")
        return False

    # Only write to file after sanity check;
    # this number is used to construct commit message in workflow.
    (Path(dir) / "LATEST_REVISION").write_text(str(rev_remote))

    m_remote.export(os.path.join(dir, "v0000.json"))
    for i in range(1, rev_remote):
        gom.fetch(i, pc=pc).export(os.path.join(dir, f"v{i:04}.json"))

    return True


if __name__ == "__main__":
    # if any run returns True, exit with 0
    sys.exit(not (do_update("manifests") or do_update("manifests_pc", pc=True)))
