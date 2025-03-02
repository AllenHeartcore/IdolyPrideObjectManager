"""
update_manifest.py
Script to fetch latest manifest and diff from server,
compatible with 'Update Manifest' workflow.
"""

import GkmasObjectManager as gom


def main():

    m_remote = gom.fetch()
    m_local = gom.load("manifests/v0000.json")

    if m_remote.revision == m_local.revision:
        print("No update available.")
        return -1

    latest_revision = m_remote.revision._get_canon_repr()
    m_remote.export(f"manifests/v0000.json")

    for i in range(1, latest_revision):
        gom.fetch(i).export(f"manifests/v{i:04}.json")

    return latest_revision


if __name__ == "__main__":
    main()
