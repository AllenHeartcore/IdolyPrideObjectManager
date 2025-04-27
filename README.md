# IdolyPrideObjectManager

An OOP interface for interacting with object databases
in the mobile game [IDOLY PRIDE](https://idolypride.jp/).

Designed with ❤ by [Ziyuan "Heartcore" Chen](https://allenheartcore.github.io/). <br>
Refactored from [gkmasToolkit](https://github.com/kishidanatsumi/gkmasToolkit) by Kishida Natsumi, <br>
which in turn was adapted from [SolisClient](https://github.com/MalitsPlus/SolisClient) by Vibbit. <br>
Request API & decryption algorithms borrowed from [HatsuboshiToolkit](https://github.com/DreamGallery/HatsuboshiToolkit) by DreamGallery.



## Features

- Fetch, decrypt, deserialize, and export manifest as ProtoDB, JSON, or CSV
- Differentiate between manifest revisions
- Download and deobfuscate assetbundles and resources in parallel
- Media conversion plugins for Texture2D, AudioClip audio, AWB audio, and USM video



## Example Usage

```python
import IdolyPrideObjectManager as ipom

m = ipom.fetch()  # fetch latest
m.export("manifest.json")

m_old = ipom.load("octocacheevai")
m_diff = m - m_old
m_diff.export("manifest_diff.json")

m.download(
    "img.*cidol.*full.*", "img.*csprt.*full.*",  # character & support cards
    image_format="JPEG", image_resize="16:9"
)
m.download("sud.*inst.*.awb", audio_format="WAV")  # instrumental songs
m.download("mov.*cidol.*loop.usm", video_format="MP4")  # animated character cards
```



## Class Hierarchy

- `manifest.decrypt.AESCBCDecryptor` - Manifest decryption
- `manifest.octodb_pb2.Database` - ProtoDB deserialization
- `manifest.manifest.PrideManifest` - **ENTRY POINT**
  - `manifest.revision.PrideManifestRevision` - Manifest revision management
  - `manifest.listing.PrideObjectList` - Object listing and indexing
    - `object.resource.PrideResource` - Non-Unity object
      - `media.dummy.PrideDummyMedia` - Base class for media conversion plugins
      - `media.image.PrideImage` - PNG image handling
      - `media.audio.PrideAudio` - MP3 audio handling
      - `media.audio.PrideAWBAudio` - ACB/AWB audio conversion
      - `media.video.PrideUSMVideo` - USM video conversion
    - `object.deobfuscate.PrideAssetBundleDeobfuscator`
    - `object.assetbundle.PrideAssetBundle` - Unity object
      - `media.dummy.PrideDummyMedia`
      - `media.image.PrideUnityImage` - Texture2D image handling
      - `media.audio.PrideUnityAudio` - AudioClip audio handling
