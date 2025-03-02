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
        return

    for i in range(m_remote.revision._get_canon_repr()):
        gom.fetch(i).export(f"manifests/v{i:04}.json")


if __name__ == "__main__":
    main()
