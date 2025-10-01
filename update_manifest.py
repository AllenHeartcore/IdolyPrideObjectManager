"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import asyncio
import sys
from pathlib import Path

import IdolyPrideObjectManager as ipom


def fetch_one(rev: int):
    ipom.fetch(rev).export(f"manifests/v{rev:04}.json", force_overwrite=True)


async def do_update(path: str) -> bool:
    """Check for manifest update from server and optionally update all diff revisions."""

    path = Path(path)
    m_remote = ipom.fetch()
    rev_remote = m_remote.revision.canon_repr
    rev_local = int((path / "LATEST_REVISION").read_text())

    if rev_remote == rev_local:
        print("No update available.")
        return False

    # Only write to file after sanity check;
    # this number is used to construct commit message in workflow.
    (path / "LATEST_REVISION").write_text(str(rev_remote))

    m_remote.export(path / "v0000.json", force_overwrite=True)
    await asyncio.gather(
        *[asyncio.to_thread(fetch_one, i) for i in range(1, rev_remote)]
    )

    return True


if __name__ == "__main__":
    HAS_UPDATE = asyncio.run(do_update("manifests"))
    sys.exit(not (HAS_UPDATE))
