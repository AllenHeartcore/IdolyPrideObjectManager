"""
GkmasObjectManager
==================
Written by Ziyuan Chen (https://github.com/AllenHeartcore/gkmasToolkit_core).
Refactored from Kishida Natsumi (https://github.com/kishidanatsumi/gkmasToolkit),
which in turn was adapted from Vibbit (https://github.com/MalitsPlus/HoshimiToolkit).

This module defines an object-oriented interface for interacting with object databases
in the mobile game Gakuen Idolm@ster (https://gakuen.idolmaster-official.jp/).
"""

from .manifest import GkmasManifest, load
from .object import GkmasAssetBundle, GkmasResource
