"""
_initdb.py
[CLASS SPLIT] GkmasManifest protobuf initialization.
"""

from ..utils import Diclist, Logger
from ..const import (
    PATH_ARGTYPE,
    GKMAS_API_URL,
    GKMAS_API_HEADER,
    GKMAS_ONLINEPDB_KEY,
    GKMAS_OCTOCACHE_KEY,
    GKMAS_OCTOCACHE_IV,
)

from .crypt import AESCBCDecryptor
from .octodb_pb2 import Database as ProtoDB
from ..object import GkmasAssetBundle, GkmasResource

import requests
from pathlib import Path
from urllib.parse import urljoin
from google.protobuf.json_format import MessageToDict


logger = Logger()


def _online_init(self, revision: int = 0):
    """
    [INTERNAL] Requests a manifest by the specified revision.
    Algorithm courtesy of github.com/DreamGallery/HatsuboshiToolkit
    """
    url = urljoin(GKMAS_API_URL, str(revision))
    enc = requests.get(url, headers=GKMAS_API_HEADER).content
    cipher = AESCBCDecryptor(GKMAS_ONLINEPDB_KEY, enc[:16])
    dec = cipher.process(enc[16:])
    self._parse_raw(dec)
    logger.info("Manifest created from online ProtoDB")


def _offline_init(self, src: PATH_ARGTYPE):
    """
    [INTERNAL] Initializes a manifest from the given offline source.
    The protobuf referred to can be either encrypted or not.
    """
    enc = Path(src).read_bytes()
    try:
        self._parse_raw(enc)
        logger.info("Manifest created from unencrypted ProtoDB")
    except:
        cipher = AESCBCDecryptor(GKMAS_OCTOCACHE_KEY, GKMAS_OCTOCACHE_IV)
        dec = cipher.process(enc)
        self._parse_raw(dec[16:])  # trim md5 hash
        logger.info("Manifest created from encrypted ProtoDB")


def _parse_raw(self, raw: bytes):
    """
    [INTERNAL] Records raw protobuf bytes, converts to JSON,
    and calls "secondary backend" JSON parser.
    """
    pdb = ProtoDB()
    pdb.ParseFromString(raw)
    self.revision = pdb.revision
    # Not moved to _parse_jdict(), since manifest from diff
    # (__sub__ magic method) manually records revision before calling it.
    self._parse_jdict(MessageToDict(pdb))


def _parse_jdict(self, jdict: dict):
    """
    [INTERNAL] Parses the JSON dictionary into internal structures.
    Also *directly* called from _make_diff_manifest(),
    without handling raw protobuf in advance.

    Internal attributes:
        _abl (Diclist): List of assetbundle *info dictionaries*.
        _resl (Diclist): List of resource *info dictionaries*.
        _name2object (dict): Mapping from object name to GkmasAssetBundle/GkmasResource.

    Documentation for Diclist can be found in utils.py.
    """
    jdict["assetBundleList"] = sorted(jdict["assetBundleList"], key=lambda x: x["id"])
    jdict["resourceList"] = sorted(jdict["resourceList"], key=lambda x: x["id"])
    self.jdict = jdict
    self._abl = Diclist(self.jdict["assetBundleList"])
    self._resl = Diclist(self.jdict["resourceList"])
    self.abs = [GkmasAssetBundle(ab) for ab in self._abl]
    self.reses = [GkmasResource(res) for res in self._resl]
    self._name2object = {ab.name: ab for ab in self.abs}  # quick lookup
    self._name2object.update({res.name: res for res in self.reses})
    logger.info(f"Found {len(self.abs)} assetbundles")
    logger.info(f"Found {len(self.reses)} resources")
    logger.info(f"Detected revision: {self.revision}")
