"""
IdolyPrideObjectManager
==================
Written by Ziyuan Chen (https://github.com/AllenHeartcore/IdolyPrideObjectManager).
Refactored from Kishida Natsumi (https://github.com/kishidanatsumi/gkmasToolkit),
which in turn was adapted from Vibbit (https://github.com/MalitsPlus/SolisClient).

This module defines an object-oriented interface for interacting with object databases
(hereafter referred to as "manifests", usually named "octocacheevai")
in the mobile game [IDOLY PRIDE](https://idolypride.jp/).

Features
--------
- Decrypt and export octocache as raw ProtoDB, JSON, or CSV
- Differentiate between octocache revisions
- Download and deobfuscate objects in parallel

Example Usage
-------------
```python
from IdolyPrideObjectManager import PrideManifest
manifest = PrideManifest("EncryptedCache/octocacheevai")
manifest.export('DecryptedCache/')
manifest.download('adv.*ttmr.*', 'sud_vo.*fktn.*', 'mdl.*hski.*')

manifest_old = PrideManifest("EncryptedCache/octocacheevai_old")
mdiff = manifest - manifest_old
mdiff.export('DecryptedCache/diff/')
```
"""

from .manifest import PrideManifest, fetch, load
from .object import PrideAssetBundle, PrideResource
