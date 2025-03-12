"""
GkmasObjectManager
==================
Written by Ziyuan Chen (https://github.com/AllenHeartcore/gkmasToolkit_core).
Refactored from Kishida Natsumi (https://github.com/kishidanatsumi/gkmasToolkit),
which in turn was adapted from Vibbit (https://github.com/MalitsPlus/HoshimiToolkit).

This module defines an object-oriented interface for interacting with object databases
(hereafter referred to as "manifests", usually named "octocacheevai")
in the mobile game Gakuen Idolm@ster (https://gakuen.idolmaster-official.jp/).

Features
--------
- Export octocache as raw ProtoDB or JSON
- Differentiate between octocache revisions
- Download and deobfuscate objects in parallel

Example Usage
-------------
```python
from GkmasObjectManager import GkmasManifest
manifest = GkmasManifest("octocacheevai")
manifest.export('manifest.json')
manifest.download('adv.*ttmr.*', 'sud_vo.*fktn.*', 'mdl.*hski.*', nworker=8)

manifest_old = GkmasManifest("octocacheevai_old")
mdiff = manifest - manifest_old
mdiff.export('manifest_diff.json')
```
"""

from .manifest import GkmasManifest, fetch, load
from .object import GkmasAssetBundle, GkmasResource
