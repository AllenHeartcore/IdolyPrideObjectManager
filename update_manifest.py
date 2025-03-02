"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import GkmasObjectManager as gom

import sys


def main():

    m_remote = gom.fetch()
    latest_revision = m_remote.revision._get_canon_repr()

    m_local = gom.load("manifests/v0000.json")
    if m_remote.revision == m_local.revision:
        print("No update available.")
        sys.exit(-1)

    # Only write to file after sanity check;
    # this number is only used to construct commit message in workflow
    # but not used to determine local manifest revision.
    with open("manifests/LATEST_REVISION", "w") as f:
        f.write(str(latest_revision))

    m_remote.export(f"manifests/v0000.json")
    for i in range(1, latest_revision):
        gom.fetch(i).export(f"manifests/v{i:04}.json")

    sys.exit(0)


if __name__ == "__main__":
    main()
