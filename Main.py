from GkmasObjectManager import GkmasManifest


manifest = GkmasManifest("EncryptedCache/octocacheevai_v81")
manifest.export("DecryptedCache/v81")
manifest.download_all()
