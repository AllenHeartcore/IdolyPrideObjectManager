"""
const.py
Module-wide constants (macro equivalents).
"""

from pathlib import Path
from urllib.parse import urljoin

from .utils import md5sum

# argument type hints
PathArgtype = str | Path

# manifest request
PRIDE_APPID = 212
PRIDE_VERSION = 205051
PRIDE_API_SERVER = "https://api.octo-cloud.com/"
PRIDE_API_URL = urljoin(
    PRIDE_API_SERVER, f"v2/pub/a/{PRIDE_APPID}/v/{PRIDE_VERSION}/list/"
)
PRIDE_API_KEY = "xop8c3tqrl8dcgij6mc9y4yf5o7btknt"
PRIDE_API_HEADER = {
    "Accept": f"application/x-protobuf,x-octo-app/{PRIDE_APPID}",
    "X-OCTO-KEY": PRIDE_API_KEY,
}

# manifest decrypt
PRIDE_ONLINEPDB_KEY = bytes.fromhex(
    "aa8a30926db9d49410360d0a99aa735d035638dfc09ef99fb575d9c91a8f6cdc"
)
PRIDE_ONLINEPDB_IV = bytes.fromhex("9ce1286f5481bb3d92eb8529bc35962c")
PRIDE_OCTOCACHE_KEY = md5sum("zkfuuwgc4eoxlaew".encode("utf-8"))
PRIDE_OCTOCACHE_IV = md5sum("LvAUtf+tnz".encode("utf-8"))

# manifest history
REPO_OBJECT_URL_TEMPLATE = "https://raw.githubusercontent.com/AllenHeartcore/IdolyPrideObjectManager/{branch}/{path}"
MANIFEST_UPDATE_BRANCH = "manifest-update"
WAYBACK_COMMITS_LOG_LOCAL = "wayback_commits.json"
WAYBACK_COMMITS_LOG_REMOTE = REPO_OBJECT_URL_TEMPLATE.format(
    branch=MANIFEST_UPDATE_BRANCH, path=WAYBACK_COMMITS_LOG_LOCAL
)
WAYBACK_OBJECTS_LOG_LOCAL = "wayback_objects.json"
WAYBACK_OBJECTS_LOG_REMOTE = REPO_OBJECT_URL_TEMPLATE.format(
    branch=MANIFEST_UPDATE_BRANCH, path=WAYBACK_OBJECTS_LOG_LOCAL
)
WAYBACK_MANIFEST_URL_TEMPLATE = REPO_OBJECT_URL_TEMPLATE.format(
    branch="{hash}", path="manifests/v{revision:04d}.json"
)
