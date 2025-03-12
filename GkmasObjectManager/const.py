"""
const.py
Module-wide constants (macro equivalents).
"""

import multiprocessing
from hashlib import md5, sha256
from pathlib import Path
from typing import Union, Tuple


# argument type hints
PATH_ARGTYPE = Union[str, Path]
IMAGE_RESIZE_ARGTYPE = Union[None, str, Tuple[int, int]]

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
OBJLIST_ID_FIELD = "id"
OBJLIST_NAME_FIELD = "name"

# manifest export
CSV_COLUMNS = ["objectName", "md5", "name", "size", "state"]

# manifest download dispatcher
DEFAULT_DOWNLOAD_PATH = "objects/"
DEFAULT_DOWNLOAD_NWORKER = multiprocessing.cpu_count()

# object instantiation
RESOURCE_INFO_FIELDS_HEAD = ["id", "name", "size"]
RESOURCE_INFO_FIELDS_TAIL = ["state", "md5", "objectName", "uploadVersionId"]
RESOURCE_INFO_FIELDS = RESOURCE_INFO_FIELDS_HEAD + RESOURCE_INFO_FIELDS_TAIL

# object download
GKMAS_OBJECT_SERVER = "https://object.asset.game-gakuen-idolmaster.jp/"
CHARACTER_ABBREVS = [
    "hski",  # Hanami SaKI
    "ttmr",  # Tsukimura TeMaRi
    "fktn",  # Fujita KoToNe
    "amao",  # Arimura MAO
    "kllj",  # Katsuragi LiLJa
    "kcna",  # Kuramoto ChiNA
    "ssmk",  # Shiun SuMiKa
    "shro",  # Shinosawa HiRO
    "hrnm",  # Himesaki RiNaMi
    "hume",  # Hanami UME
    "hmsz",  # Hataya MiSuZu
    "jsna",  # Juo SeNA
    "atbm",  # Amaya TsuBaMe
    "jkno",  # Juo KuNiO
    "nasr",  # Neo ASaRi
    "trvo",  # VOcal TRainer
    "trda",  # DAnce TRainer
    "trvi",  # VIsual TRainer
    "krnh",  # Kayo RiNHa
    "andk",  # Aoi NaDeshiKo
    "sson",  # Shirakusa ShiON
    "sgka",  # Shirakusa GekKA
    "ktko",  # Kuroi TaKaO
    "cmmn",  # (CoMMoN)
]
