"""
IdolyPrideObjectManager
An object-oriented interface for interacting with object databases ("manifests")
in the mobile game [IDOLY PRIDE](https://idolypride.jp/)
"""

from .manifest import PrideManifest, fetch, load
from .object import PrideAssetBundle, PrideResource
