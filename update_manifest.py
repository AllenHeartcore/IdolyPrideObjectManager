"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import IdolyPrideObjectManager as ipom

import sys
from pathlib import Path


def do_update(dir: str, pc: bool = False) -> bool:

    dir = Path(dir)
    m_remote = ipom.fetch(pc=pc)
    rev_remote = m_remote.revision._get_canon_repr()
    rev_local = int((dir / "LATEST_REVISION").read_text())

    if rev_remote == rev_local:
        print("No update available.")
        return False

    # Only write to file after sanity check;
    # this number is used to construct commit message in workflow.
    (dir / "LATEST_REVISION").write_text(str(rev_remote))

    m_remote.export(dir / "v0000.json")
    for i in range(1, rev_remote):
        ipom.fetch(i, pc=pc).export(dir / f"v{i:04}.json")

    return True


if __name__ == "__main__":
    has_update = do_update("manifests")
    has_update_pc = do_update("manifests_pc", pc=True)
    sys.exit(not (has_update or has_update_pc))  # avoids short-circuiting
