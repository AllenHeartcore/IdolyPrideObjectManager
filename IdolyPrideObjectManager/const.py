"""
const.py
Module-wide constants (macro equivalents).
"""

from pathlib import Path
from typing import Union
from urllib.parse import urljoin

from .utils import md5sum

# argument type hints
PathArgtype = Union[str, Path]

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

# manifest export
CSV_COLUMNS = [
    "objectName",
    "generation",
    "md5",
    "name",
    "size",
    "state",
]

# manifest download dispatcher
DEFAULT_DOWNLOAD_PATH = "objects/"

# object download
CHARACTER_ABBREVS = [
    "mna",  # nagase MaNA
    # Tsuki no tempest
    "ktn",  # nagase KoToNo
    "ngs",  # ibuki NaGiSa
    "ski",  # shiraishi SaKI
    "suz",  # narumiya SUZu
    "mei",  # hayasaka MEI
    # Sunny peace
    "skr",  # kawasaki SaKuRa
    "szk",  # hyodo ShiZuKu
    "chs",  # shiraishi CHiSa
    "rei",  # ichinose REI
    "hrk",  # saeki HaRuKo
    # TRINITYAiLE
    "rui",  # tendo RUI
    "yu",  # suzumura YU
    "smr",  # okuyama SuMiRe
    # LizNoir
    "rio",  # kanzaki RIO
    "aoi",  # igawa AOI
    "ai",  # komiyama AI
    "kkr",  # akazaki KoKoRo
    # IIIX
    "kor",  # yamada "fran"ziska KaORi
    "kan",  # kojima "KANa"
    "mhk",  # takeda "MiHo"Ko
    # (Collab)
    "mku",  # hatsune MiKU
    "ymk",  # Yuki MiKu
    "chk",  # takami CHiKa
    "rik",  # sakurauchi RIKo
    "yo",  # watanabe YOu
    "cca",  # hoto CoCoA
    "chn",  # kafu CHiNo
]

# object deobfuscate
PRIDE_UNITY_VERSION = "2022.3.21f1"
UNITY_SIGNATURE = b"UnityFS"

# adventure captioning
DEFAULT_USERNAME = "マネージャー"
