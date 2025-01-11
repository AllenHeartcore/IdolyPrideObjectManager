"""
const.py
Module-wide constants (macro equivalents).
"""

import multiprocessing
from hashlib import md5, sha256
from pathlib import Path
from typing import Union, Tuple


# client-side visible control tokens
# that start with '<' and end with '>' (prohibited in Windows paths)
ALL_ASSETBUNDLES = "<ALL_ASSETBUNDLES>"
ALL_RESOURCES = "<ALL_RESOURCES>"
VERSION = lambda x: f"<{x:d}>"
LATEST = VERSION(0)

# argument type hints
PATH_ARGTYPE = Union[str, Path]
IMG_RESIZE_ARGTYPE = Union[None, str, Tuple[int, int]]

# manifest request
GKMAS_APPID = 400
GKMAS_VERSION = 205000
GKMAS_API_SERVER = f"https://api.asset.game-gakuen-idolmaster.jp/"
GKMAS_API_URL = f"{GKMAS_API_SERVER}/v2/pub/a/{GKMAS_APPID}/v/{GKMAS_VERSION}/list/"
GKMAS_API_KEY = "0jv0wsohnnsigttbfigushbtl3a8m7l5"
GKMAS_API_HEADER = {
    "Accept": f"application/x-protobuf,x-octo-app/{GKMAS_APPID}",
    "X-OCTO-KEY": GKMAS_API_KEY,
}

# manifest decrypt
sha256sum = lambda x: sha256(bytes(x, "utf-8")).digest()
md5sum = lambda x: md5(bytes(x, "utf-8")).digest()
GKMAS_ONLINEPDB_KEY = sha256sum("eSquJySjayO5OLLVgdTd")
GKMAS_OCTOCACHE_KEY = md5sum("1nuv9td1bw1udefk")
GKMAS_OCTOCACHE_IV = md5sum("LvAUtf+tnz")

# manifest diff
DICLIST_INDEX_FIELD = "id"
DICLIST_NAME_FIELD = "name"
DICLIST_DIFF_IGNORED_FIELDS = ["dependencies", "uploadVersionId"]

# manifest export
CSV_COLUMNS = ["objectName", "md5", "name", "size", "state"]

# manifest download dispatcher
DEFAULT_DOWNLOAD_PATH = "objects/"
DEFAULT_DOWNLOAD_NWORKER = multiprocessing.cpu_count()

# object download
GKMAS_OBJECT_SERVER = "https://object.asset.game-gakuen-idolmaster.jp/"
CHARACTER_ABBREVS = [
    "hski",  # Hanami SaKI
    "ttmr",  # Tsukimura TeMaRi
    "fktn",  # Fujita KoToNe
    "hrnm",  # Himesaki RiNaMi
    "ssmk",  # Shiun SuMiKa
    "shro",  # Shinosawa HiRO
    "kllj",  # Katsuragi LiLJa
    "kcna",  # Kuramoto ChiNA
    "amao",  # Arimura MAO
    "hume",  # Hanami UME
    "hmsz",  # Hataya MiSuZu
    "jsna",  # Juo SeNA
    "nasr",  # Neo ASaRi
    "trvo",  # VOcal TRainer
    "trda",  # DAnce TRainer
    "trvi",  # VIsual TRainer
]

# object deobfuscate
GKMAS_UNITY_VERSION = "2022.3.21f1"
UNITY_SIGNATURE = b"UnityFS"
