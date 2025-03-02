"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import GkmasObjectManager as gom

import sys
from pathlib import Path


def main():

    m_remote = gom.fetch()
    rev_remote = m_remote.revision._get_canon_repr()
    rev_local = int(Path("manifests/LATEST_REVISION").read_text())

    if rev_remote == rev_local:
        print("No update available.")
        sys.exit(-1)

    # Only write to file after sanity check;
    # this number is used to construct commit message in workflow.
    Path("manifests/LATEST_REVISION").write_text(str(rev_remote))

    m_remote.export(f"manifests/v0000.json")
    for i in range(1, rev_remote):
        gom.fetch(i).export(f"manifests/v{i:04}.json")

    sys.exit(0)


if __name__ == "__main__":
    main()
