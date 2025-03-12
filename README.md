# GkmasObjectManager

An OOP interface for interacting with object databases
in the mobile game [Gakuen Idolm@ster](https://gakuen.idolmaster-official.jp/).

Designed with ❤ by [Ziyuan "Heartcore" Chen](https://allenheartcore.github.io/). <br>
Refactored from [gkmasToolkit](https://github.com/kishidanatsumi/gkmasToolkit) by Kishida Natsumi, <br>
which in turn was adapted from [HoshimiToolkit](https://github.com/MalitsPlus/HoshimiToolkit) by Vibbit. <br>
Request API & decryption algorithms borrowed from [HatsuboshiToolkit](https://github.com/DreamGallery/HatsuboshiToolkit) by DreamGallery.



## Features

- Fetch, decrypt, deserialize, and export manifest as ProtoDB, JSON, or CSV
- Differentiate between manifest revisions
- Download and deobfuscate assetbundles and resources in parallel
- Media conversion plugins for Texture2D, AudioClip audio, AWB audio, and USM video



## Example Usage

```python
import GkmasObjectManager as gom

m = gom.fetch()  # fetch latest
m.export("manifest.json")

m_old = gom.load("octocacheevai")
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
- `manifest.manifest.GkmasManifest` - **ENTRY POINT**
  - `manifest.revision.GkmasManifestRevision` - Manifest revision management
  - `manifest.listing.GkmasObjectList` - Object listing and indexing
    - `object.resource.GkmasResource` - Non-Unity object
      - `media.dummy.GkmasDummyMedia` - Base class for media conversion plugins
      - `media.image.GkmasImage` - PNG image handling
      - `media.audio.GkmasAudio` - MP3 audio handling
      - `media.audio.GkmasAWBAudio` - ACB/AWB audio conversion
      - `media.video.GkmasUSMVideo` - USM video conversion
    - `object.deobfuscate.GkmasAssetBundleDeobfuscator`
    - `object.assetbundle.GkmasAssetBundle` - Unity object
      - `media.dummy.GkmasDummyMedia`
      - `media.image.GkmasUnityImage` - Texture2D image handling
      - `media.audio.GkmasUnityAudio` - AudioClip audio handling
      - `media.ai_caption.GPTCaptionEngine` - Image and video captioning



## Object Hierarchy

`#` denotes a number. <br>
`IDOL` denotes `(hski|ttmr|fktn|amao|kllj|kcna|ssmk|shro|hrnm|hume|hmsz|jsna)`.

- Image `img`
  - `adv`
    - `img_adv_speaker_(krnh|andk|sson|sgka)_###-###`
    - `img_adv_still_all_cmmn_###-##`
    - `img_adv_still_dear_IDOL_###-###`
    - `img_adv_still_pstory_cmmn_###-##`
  - `chr`
    - `img_chr_IDOL_##-(audition|bustup|full|thumb-circle|thumb-push)`
    - `img_chr_(atbm|nasr|trvo|trda|trvi)_##-thumb-circle`
  - `cos`
    - `img_cos_IDOL-(schl|trng|casl|cstm|othr)-####_body`
    - `img_cos_costume_head_IDOL-(schl|casl|cstm|hair)-####_head`
  - `gasha`
    - `img_gasha_banner_gasha-#####-(standard|pickup|select-pickup|free)-###-(logo|select|select-m|select-s)`
    - `img_gasha_banner_gasha-#####-(pidol|support)-select-pickup-###-(logo|select-m|select-s)`
    - `img_gasha_banner_gasha_ticket_ssr_(idol|support|idol_support)_#-(logo|select-m|select-s)`
    - `img_gasha_banner_gasha_ssr_##-(logo|select-m|select-s)`
    - `img_gasha_text_*`
  - `general`
    - `img_general_achievement_(common|produce|char_IDOL)_###`
    - `img_general_achievement_IDOL-(#-###|master|tower)_###`
    - `img_general_cidol-IDOL-#-###_#-(full|thumb-(landscape|landscape-large|portrait|square|gasha))`
    - `img_general_csprt-1-####_(full|thumb-(landscape|square))`
    - `img_general_(comic_####|comic4_####|comic4_####-thumb)`
    - `img_general_commu_(top|part|support|event)-header_###`
    - `img_general_commu_chapter-(header|thumb)_##-##`
    - `img_general_commu_thumb_unit_##-##-##`
    - `img_general_commu_idol-top_IDOL-thumb`
    - `img_general_commu_dearness_IDOl-banner`
    - ...
  - ...
- Audio `sud`
  - ...
- Video `mov`
  - `mov_adv_dear_ed_IDOL_###`
  - `mov_adv_unit_explanation_cmmn_###`
  - `mov_gasha_monitor_(monitor|step1|tap)-(000|002|003|004_IDOL)`
  - `mov_gasha_movie_tap-(000|002|003|004)`
  - ...
- Text `adv`
  - ...
- Models
  - Model `mdl`
    - ...
  - Motion `mot`
    - ...
  - Environment `env`
    - ...
  - FBX `fbx`
  - MEF `mef`
  - Timeline `tln`
  - Crowd `crw`
  - Effect `eff`
- Miscellaneous
  - `scl`
  - `ttn`
  - `fgd`
  - `t`
  - `sky`
  - `image_sprite_atlas.unity3d`
  - `actor-shader.unity3d`
  - `ui-shader.unity3d`
  - `shader.unity3d`
  - `m_fdc.unity3d`
  - `Custom.acf`
  - `musics.txt`
