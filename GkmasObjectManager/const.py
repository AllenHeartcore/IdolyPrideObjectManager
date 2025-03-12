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

GKMAS_VERSION = 205000

# manifest diff
OBJLIST_ID_FIELD = "id"
OBJLIST_NAME_FIELD = "name"

# object instantiation
RESOURCE_INFO_FIELDS_HEAD = ["id", "name", "size"]
RESOURCE_INFO_FIELDS_TAIL = ["state", "md5", "objectName", "uploadVersionId"]
RESOURCE_INFO_FIELDS = RESOURCE_INFO_FIELDS_HEAD + RESOURCE_INFO_FIELDS_TAIL

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
