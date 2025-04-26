"""
const.py
Module-wide constants (macro equivalents).
"""

from pathlib import Path
from urllib.parse import urljoin
from typing import Union, Tuple
from cryptography.hazmat.primitives import hashes


def sha256sum(data: bytes) -> bytes:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()


def md5sum(data: bytes) -> bytes:
    digest = hashes.Hash(hashes.MD5())
    digest.update(data)
    return digest.finalize()


# argument type hints
PATH_ARGTYPE = Union[str, Path]
IMAGE_RESIZE_ARGTYPE = Union[None, str, Tuple[int, int]]

# manifest request
PRIDE_APPID = 400
PRIDE_VERSION = 205000
PRIDE_VERSION_PC = 705000
PRIDE_API_SERVER = f"https://api.asset.game-gakuen-idolmaster.jp/"
PRIDE_API_URL = urljoin(
    PRIDE_API_SERVER, f"v2/pub/a/{PRIDE_APPID}/v/{PRIDE_VERSION}/list/"
)
PRIDE_API_URL_PC = urljoin(
    PRIDE_API_SERVER, f"v2/pub/a/{PRIDE_APPID}/v/{PRIDE_VERSION_PC}/list/"
)
PRIDE_API_KEY = "0jv0wsohnnsigttbfigushbtl3a8m7l5"
PRIDE_API_HEADER = {
    "Accept": f"application/x-protobuf,x-octo-app/{PRIDE_APPID}",
    "X-OCTO-KEY": PRIDE_API_KEY,
}

# manifest decrypt
PRIDE_ONLINEPDB_KEY = sha256sum("eSquJySjayO5OLLVgdTd".encode("utf-8"))
PRIDE_ONLINEPDB_KEY_PC = sha256sum("x5HFaJCJywDyuButLM0f".encode("utf-8"))
PRIDE_OCTOCACHE_KEY = md5sum("1nuv9td1bw1udefk".encode("utf-8"))
PRIDE_OCTOCACHE_IV = md5sum("LvAUtf+tnz".encode("utf-8"))

# manifest diff
OBJLIST_ID_FIELD = "id"
OBJLIST_NAME_FIELD = "name"

# manifest export
CSV_COLUMNS = ["objectName", "md5", "name", "size", "state"]

# manifest download dispatcher
DEFAULT_DOWNLOAD_PATH = "objects/"

# object instantiation
RESOURCE_INFO_FIELDS_HEAD = ["id", "name", "size"]
RESOURCE_INFO_FIELDS_TAIL = ["state", "md5", "objectName", "uploadVersionId"]
RESOURCE_INFO_FIELDS = RESOURCE_INFO_FIELDS_HEAD + RESOURCE_INFO_FIELDS_TAIL

# object download
PRIDE_OBJECT_SERVER = "https://object.asset.game-gakuen-idolmaster.jp/"
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

# object deobfuscate
PRIDE_UNITY_VERSION = "2022.3.21f1"
UNITY_SIGNATURE = b"UnityFS"
