# GkmasObjectManager-demo

A CRUD-compatible demo build of the [GkmasObjectManager](https://github.com/AllenHeartcore/GkmasObjectManager) project,
which provides an OOP-style Python interface for interacting with object databases
in the mobile game [Gakuen Idolm@ster](https://gakuen.idolmaster-official.jp/).

Designed with ❤ by [Ziyuan "Heartcore" Chen](https://allenheartcore.github.io/).



<br>

## Comparing Features

| | Demo Build | Full Build |
| --- | --- | --- |
| Branch | [`offline-demo`](https://github.com/AllenHeartcore/GkmasObjectManager/tree/offline-demo) | [`main`](https://github.com/AllenHeartcore/GkmasObjectManager/tree/main) |
| CRUD Support | CRU | R |
| # Entries | 111 | 23,016 (as of manifest revision 201) |
| Manifest | JSON load <br> JSON export <br> Differentiate <br> Search by regex | Online fetch & decrypt <br> ProtoDB, JSON load <br> ProtoDB, JSON, CSV export <br> Differentiate <br> Search by regex <br> Multiprocess download |
| Object | Resource indexing | Resource download <br> AssetBundle deobfuscate, download |
| Multimedia | PNG image <br> MP3 audio | USM video <br> Texture2D, PNG image <br> AudioClip, AWB/ACB, MP3 audio <br> GPT image captioning |



<br>

## Testing CRUD Functionality

Among the 8 attributes of each entry in `manifest.json` -- namely,
```
"id", "name", "size", "md5", "url", "cover", "keywords", "caption"
```
the `id` is assigned, `size` and `md5` are auto-generated, and the user is only allowed to modify
`name` (song title), `url` (URL to audio), `cover` (URL to cover image), `keywords` (search tags), and `caption` (image caption).

Among these five fields, `name`, `keywords`, and `caption` are free-form text
(they don't need to match existing entries or follow specific formats).
However, to maintain dataset integrity, any URLs the user provides should be from the game server.
Therefore, `url` and `cover` are enforced to be of the format `https://object.asset.game-gakuen-idolmaster.jp/{objectName}`,
and only the 6-character alphanumeric `objectName`'s are variable.

Starting from the provided 107 entries, the following table shows all the valid `objectName` values:

| ID | Action | `name` | `url` | `cover` |
| --- | --- | --- | --- | --- |
| 25 | Edit | キミとセミブルー (藤田 ことね ver.) | `JZ8G1Y` | |
| 26 | Edit | キミとセミブルー (葛城 リーリヤ ver.) | `COZKHv` | |
| 27 | Edit | キミとセミブルー (花海 咲季 ver.) | `8tllfB` | |
| 28 | Edit | キミとセミブルー (有村 麻央 ver.) | `oqiH3Q` | |
| 29 | Edit | キミとセミブルー (月村 手毬 ver.) | `Rzwcaw` | |
| 30 | Edit | キミとセミブルー (紫雲 清夏 ver.) | `dO1J7J` | |
| 31 | Edit | キミとセミブルー (姫崎 莉波 ver.) | `3kcXWe` | |
| 32 | Edit | キミとセミブルー (倉本 千奈 ver.) | `XwlZOm` | |
| 33 | Edit | キミとセミブルー (花海 佑芽 ver.) | `UMSszG` | |
| 34 | Edit | キミとセミブルー (篠澤 広 ver.) | `2DroMz` | |
| 35 | Edit | Wake up!! | `sZlsvv` | |
| 36 | Edit | コントラスト | `kmS6W2` | |
| 38 | Edit | 冠菊 (紫雲 清夏 ver.) | `s0Tnid` | |
| 39 | Edit | 冠菊 (有村 麻央 ver.) | `ctoDFI` | |
| 40 | Edit | 冠菊 (葛城 リーリヤ ver.) | `zQHVoj` | |
| 41 | Edit | 冠菊 (月村 手毬 ver.) | `B9SnrG` | |
| 42 | Edit | 冠菊 (姫崎 莉波 ver.) | `Mf9rqI` | |
| 43 | Edit | 冠菊 (花海 咲季 ver.) | `Ks5tH0` | |
| 44 | Edit | 冠菊 (倉本 千奈 ver.) | `hYUgLC` | |
| 45 | Edit | 冠菊 (篠澤 広 ver.) | `DwrrZf` | |
| 46 | Edit | 冠菊 (藤田 ことね ver.) | `9Wt6Gs` | |
| 47 | Edit | 冠菊 (花海 佑芽 ver.) | `DFwfpc` | |
| 48 | Edit | 日々、発見的ステップ！ | | `yXR7hn` |
| 67 | Edit | White Night! White Wish! (紫雲 清夏 ver.) | | `XSf0oj` |
| 68 | Edit | White Night! White Wish! (姫崎 莉波 ver.) | | `aabOep` |
| 69 | Edit | White Night! White Wish! (有村 麻央 ver.) | | `oW8UGV` |
| 70 | Edit | White Night! White Wish! (葛城 リーリヤ ver.) | | `9hrq1V` |
| 71 | Edit | White Night! White Wish! (月村 手毬 ver.) | | `ZPZVrx` |
| 72 | Edit | White Night! White Wish! (花海 咲季 ver.) | | `GGjxnQ` |
| 73 | Edit | White Night! White Wish! (篠澤 広 ver.) | | `nv9JAf` |
| 108 | Add | 雪解けに (有村 麻央 ver.) | `82gmg6` | `S5vJG8` |
| 109 | Add | 雪解けに (藤田 ことね ver.) | `fuoVaB` | `gWrBbc` |
| 110 | Add | 雪解けに (葛城 リーリヤ ver.) | `SBo1Jt` | `Q2vQXs` |
| 111 | Add | 雪解けに (花海 咲季 ver.) | `aDOafP` | `4w3kvt` |

### Side notes
- *The `objectName`'s for the "Add" action are fetched from **newer** versions of the manifest,
    while those for "Edit" are from **older** versions.*
- *Many of the updated assets would have little perceptible difference from the original ones,
    but they still slightly differ in terms of format and encoding, have different sizes and MD5 hashes,
    and therefore are still included in the demo for testing coverage.*



<br>

## Datasheet

### Character abbreviations

| Abbrev. | English Name | Japanese Name |
| --- | --- | --- |
| hski | Hanami Saki | 花海 咲季 |
| ttmr | Tsukimura Temari | 月村 手毬 |
| fktn | Fujita Kotone | 藤田 ことね |
| amao | Arimura Mao | 有村 麻央 |
| kllj | Katsuragi Lilja | 葛城 リーリヤ |
| kcna | Kuramoto China | 倉本 千奈 |
| ssmk | Shiun Sumika | 紫雲 清夏 |
| shro | Shinosawa Hiro | 篠澤 広 |
| hrnm | Himesaki Rinami | 姫崎 莉波 |
| hume | Hanami Ume | 花海 佑芽 |
| hmsz | Hataya Misuzu | 秦谷 美鈴 |
| jsna | Juo Sena | 十王 星南 |

### Song abbreviations

| Abbrev. | Title | Release Date |
| --- | --- | --- |
| all-001 | [初](https://gakuen-label.idolmaster-official.jp/discography/peq6ooiqakm) | 05/16/24 |
| all-002 | [Campus mode!!](https://gakuen-label.idolmaster-official.jp/discography/mt2_igzpcsbi) | 06/10/24 |
| all-003 | [キミとセミブルー](https://gakuen-label.idolmaster-official.jp/discography/gdfqw-4qx) | 07/02/24 |
| all-004 | [冠菊](https://gakuen-label.idolmaster-official.jp/discography/totulvzn50d1) | 08/02/24 |
| all-005 | [仮装狂騒曲](https://gakuen-label.idolmaster-official.jp/discography/2ngkuekbb_fx) | 10/01/24 |
| all-006 | [White Night! White Wish!](https://gakuen-label.idolmaster-official.jp/discography/2q-imn2uac) | 11/29/24 |
| all-007 | [ハッピーミルフィーユ](https://gakuen-label.idolmaster-official.jp/discography/ibha41ntrkq) | 02/02/25 |
| all-008 | [古今東西ちょちょいのちょい](https://gakuen-label.idolmaster-official.jp/discography/3trpzlw5fki0) | 10/30/24 |
| all-009 | [雪解けに](https://gakuen-label.idolmaster-official.jp/discography/muw9595fwfz8) | 03/01/25 |
| char-001 | (1st Single) | See Below |
| char-002 | (2nd Single) | See Below |
| char-003 | (2024-25 Birthday Single) | See Below |

### Characters' Singles

| | 1st Single | 2nd Single | Birthday Single |
| - | - | - | - |
| hski | [Fighting My Way](https://gakuen-label.idolmaster-official.jp/discography/e8t8fd7twf) <br> 05/16/24 | [Boom Boom Pow](https://gakuen-label.idolmaster-official.jp/discography/tjwnhw5jcp06) <br> 06/20/24 | |
| ttmr | [Luna say maybe](https://gakuen-label.idolmaster-official.jp/discography/ux77_l7suaev) <br> 05/16/24 | [アイヴイ](https://gakuen-label.idolmaster-official.jp/discography/87k2u7a36v) <br> 05/23/24 | [叶えたい、ことばかり](https://gakuen-label.idolmaster-official.jp/discography/7i1k50ldg) <br> 06/03/24 |
| fktn | [世界一可愛い私](https://gakuen-label.idolmaster-official.jp/discography/2zxpauv9qp) <br> 05/16/24 | [Yellow Big Bang!](https://gakuen-label.idolmaster-official.jp/discography/9ar17gq88q1) <br> 06/11/24 | |
| amao | [Fluorite](https://gakuen-label.idolmaster-official.jp/discography/g600agon3y) <br> 05/16/24 | [Feel Jewel Dream](https://gakuen-label.idolmaster-official.jp/discography/jomd4kmnko) <br> 09/21/24 | [Sweet Magic](https://gakuen-label.idolmaster-official.jp/discography/kv7j8gmlsx) <br> 01/18/25 |
| kllj | [白線](https://gakuen-label.idolmaster-official.jp/discography/0c9lqwlsq1) <br> 05/16/24 | | [Wake up!!](https://gakuen-label.idolmaster-official.jp/discography/e36tqyq9nx) <br> 07/24/24 |
| kcna | [Wonder Scale](https://gakuen-label.idolmaster-official.jp/discography/2cs4vbg-vg0) <br> 05/16/24 | [日々、発見的ステップ！](https://gakuen-label.idolmaster-official.jp/discography/grepo_5d_d) <br> 08/23/24 | [憧れをいっぱい](https://gakuen-label.idolmaster-official.jp/discography/cbut20vazxu) <br> 08/01/24 |
| ssmk | [Tame-Lie-One-Step](https://gakuen-label.idolmaster-official.jp/discography/dyh02f40s6) <br> 05/16/24 | [カクシタワタシ](https://gakuen-label.idolmaster-official.jp/discography/cbzji4pfpm) <br> 12/19/24 | [Ride on beat](https://gakuen-label.idolmaster-official.jp/discography/tzqois-ne) <br> 03/14/25 |
| shro | [光景](https://gakuen-label.idolmaster-official.jp/discography/qfvmosby0) <br> 05/16/24 | [コントラスト](https://gakuen-label.idolmaster-official.jp/discography/t81m3uu7_mm) <br> 07/23/24 | [メクルメ](https://gakuen-label.idolmaster-official.jp/discography/30p5ttnh0) <br> 12/21/24 |
| hrnm | [clumsy trick](https://gakuen-label.idolmaster-official.jp/discography/habcgw0wi5) <br> 05/16/24 | [L.U.V](https://gakuen-label.idolmaster-official.jp/discography/3e88eu-75z6) <br> 10/19/24 | [marble heart](https://gakuen-label.idolmaster-official.jp/discography/161a8ag6q) <br> 03/05/25 |
| hume | [The Rolling Riceball](https://gakuen-label.idolmaster-official.jp/discography/yj5onh47v) <br> 06/01/24 | | |
| hmsz | [ツキノカメ](https://gakuen-label.idolmaster-official.jp/discography/mnwwto509nws) <br> 02/07/25 | | [たいせつなもの](https://gakuen-label.idolmaster-official.jp/discography/eev_9051s) <br> 02/06/25 |
| jsna | [小さな野望](https://gakuen-label.idolmaster-official.jp/discography/uyu_3uvq-mjn) <br> 11/16/24 | | [Cosmetic](https://gakuen-label.idolmaster-official.jp/discography/hs0e69cjtpa) <br> 12/07/24 |

### Mapping of (characters, songs) to (tiny ID of entry, full IDs and `objectName`'s of audio and cover image)

| | hski | ttmr | fktn | amao | kllj | kcna | ssmk | shro | hrnm | hume | hmsz | jsna |
| - | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| all-001 | #9 <br> 2801/2XwKzp <br> 3052/yhayBi | #14 <br> 4014/hbiQrG <br> 2044/o9FLkP | #18 <br> 5069/bP9AvK <br> 653/hh7Xbe | #4 <br> 509/GW75By <br> 4011/4A1kdF | #11 <br> 3684/7g0i7H <br> 4837/lJvtaC | #16 <br> 4477/zRUO4g <br> 1719/nxVcoY | #2 <br> 401/w5PWAa <br> 1201/GpbeP3 | #8 <br> 1978/4VpcfE <br> 4220/dWnH5r | #10 <br> 3561/OpkPGB <br> 4544/XJXhWN | #20 <br> 5409/wu14yg <br> 5569/Y5H7Tr | | #63 <br> 8519/hjpzlx <br> 8178/sRJfuQ |
| all-002 | #78 <br> 9036/JcKg3h <br> 10481/OhaZiU | #80 <br> 9368/ihKrBb <br> 10106/o3OuT9 | #82 <br> 10295/z3DHWk <br> 9290/ftbsqm | #79 <br> 9128/QeURDO <br> 10127/SNQKjO | #83 <br> 10395/tVMEp1 <br> 11403/h39gbJ | #87 <br> 10785/6hwsYc <br> 11343/xhgBhh | #84 <br> 10618/NlhHlt <br> 11384/QBukSV | #86 <br> 10728/rYeDGU <br> 11333/DjU7mX | #81 <br> 9694/nvE3DQ <br> 9456/wy95Kv | #85 <br> 10659/2BBVnL <br> 11315/egAXzT | | #88 <br> 11154/EHCYUM <br> 10128/1yLHOx |
| all-003 | #27 <br> 6038/YB0m7z <br> 6131/OrRMyo | #29 <br> 6088/AtHvDT <br> 6113/qXbLrL | #25 <br> 6012/AYJ2pA <br> 6087/kq1n7c | #28 <br> 6039/qL8unI <br> 6045/EpLa6B | #26 <br> 6022/wJv5sH <br> 6032/FXBYyO | #32 <br> 6199/FYaKmf <br> 6249/9RBKsV | #30 <br> 6132/j1Qab4 <br> 6105/kP0N7n | #34 <br> 6266/pEdCeu <br> 6156/t48yxr | #31 <br> 6145/1N3V9q <br> 6224/BDn2lZ | #33 <br> 6214/7gklQu <br> 6227/XPCkDU | | |
| all-004 | #43 <br> 6441/cw0Qrj <br> 6342/RwCyOY | #41 <br> 6381/VgyuDb <br> 6440/Kqsvwo | #46 <br> 6589/ui8o3s <br> 6530/O21oyF | #39 <br> 6360/iP8hAg <br> 6388/VxdlGx | #40 <br> 6372/jmMFiN <br> 6364/F0DvFX | #44 <br> 6501/MQaVNL <br> 6483/6TIGo8 | #38 <br> 6353/HW3sQK <br> 6444/4wmiXH | #45 <br> 6552/cesGJT <br> 6605/4t54nF | #42 <br> 6439/EuRpwC <br> 6357/jnc63G | #47 <br> 6591/Ouy12h <br> 6488/FN31ku | | |
| all-005 | #52 <br> 7462/TlDhDi <br> 7601/sE28Fx | #54 <br> 7583/mj49Lx <br> 7544/Xm8u3N | #53 <br> 7478/4CyCUO <br> 7424/aU8Ryq | #56 <br> 7642/XjWtFp <br> 7658/f3lUu1 | #59 <br> 7701/vyelq3 <br> 7632/RikjX9 | #51 <br> 7439/RhLPE4 <br> 7448/n9eNWq | #57 <br> 7655/iHwbBm <br> 7660/58pFst | #58 <br> 7684/1aNPdC <br> 7630/nimSKD | #50 <br> 7429/4Czp4k <br> 7473/4PDln1 | #55 <br> 7598/zuQn8U <br> 7455/sy7vRj | | |
| all-006 | #72 <br> 8779/dlPH2R <br> 8862/WjwQjf | #71 <br> 8777/05CId1 <br> 8901/DLCowM | #65 <br> 8651/yXBQ6q <br> 8615/bjjCDo | #69 <br> 8733/x4jtbG <br> 8748/iNqv6M | #74 <br> 8841/jl6zaw <br> 8828/tmB8yA | #70 <br> 8736/Ce2E48 <br> 8732/xTTabF | #67 <br> 8680/5EpRrE <br> 8674/KqHNLS | #73 <br> 8822/6babM0 <br> 8891/S3uc6K | #68 <br> 8712/xgH9En <br> 8704/Yj0QDh | #66 <br> 8655/U68htf <br> 8711/UjYe8U | | |
| all-007 | #95 <br> 11564/0n548W <br> 11503/3wP4aT | #99 <br> 11642/fpOFrB <br> 11695/bDR6i2 | #91 <br> 11445/h18dRp <br> 11555/SGm0br | #94 <br> 11561/qDT0Sy <br> 11485/v0l8xI | #93 <br> 11538/OJqa9f <br> 11439/vp19Dl | #98 <br> 11637/FvqLky <br> 11618/MLMjZY | #100 <br> 11666/LpT4PB <br> 11641/A4GyTB | #90 <br> 11440/uYXGgi <br> 11519/hg41nY | #92 <br> 11456/n02u77 <br> 11534/IN2i0r | | | #97 <br> 11613/yGHiX9 <br> 11636/wfU5jE |
| all-008 | #61 <br> 7894/tImaJc <br> 7849/f45532 | | | | | | | | | | | |
| all-009 | #111 <br> 11958/aDOafP <br> 11925/4w3kvt | #104 <br> 11794/cJiTfa <br> 11765/3fGmLU | #109 <br> 11922/fuoVaB <br> 11982/gWrBbc | #108 <br> 11853/82gmg6 <br> 11944/S5vJG8 | #110 <br> 11924/SBo1Jt <br> 11874/Q2vQXs | #106 <br> 11831/4rVNwE <br> 11753/g1jieV | #103 <br> 11783/0kJ8SB <br> 11761/MyGD2F | #101 <br> 11736/DIq3HO <br> 11807/V6Jt8Z | #105 <br> 11815/M9e5Kc <br> 11734/hc9Ai7 | | | #102 <br> 11771/ceeSei <br> 11743/zx4k0A |
| char-001 | #15 <br> 4402/XgdHr5 <br> 4024/ZYsGCF | #17 <br> 4501/cdbxSq <br> 1191/CP4iJ9 | #12 <br> 3749/W6ON4S <br> 1579/J2NTIN | #3 <br> 446/ANP5Zv <br> 1533/K3CkhM | #6 <br> 1430/5haOjB <br> 2382/91RRxv | #13 <br> 3971/5MzeaA <br> 2813/WutVKB | #7 <br> 1599/fEdTT4 <br> 2365/zmx1fz | #1 <br> 305/m0qJcG <br> 1542/ovW1SK | #5 <br> 1365/5mlGzP <br> 4855/tUhojr | #22 <br> 5514/2YGtSW <br> 5642/VJc7E7 | | #64 <br> 8539/sQbGdO <br> 8533/dNjR9a |
| char-002 | #24 <br> 5960/eohASs <br> 5926/OUDtVU | #19 <br> 5194/YgoIEZ <br> 5218/SW5FF6 | #23 <br> 5897/irX6uY <br> 5864/2pCWtr | #49 <br> 7369/SqqkmU <br> 7370/fOVnnm | | #48 <br> 6629/xaAnOw <br> 6648/lpoQEU | #76 <br> 8957/2CskIB <br> 8955/dukato | #36 <br> 6309/1eimkl <br> 6284/dxG4vp | #60 <br> 7802/E1XfyG <br> 7810/4RMYOI | | | |
| char-003 | | #21 <br> 5486/8nQSb9 <br> 5684/YirS2H | | #89 <br> 11409/C3pZwu <br> 11406/83hTrF | #35 <br> 6288/ecw8YE <br> 6295/2tPeQ2 | #37 <br> 6329/OtKwhl <br> 6326/w6gLbO | #62 <br> 7906/KphPXs <br> 7904/ioZg2h | #77 <br> 8970/fsmlUB <br> 8976/ilOnN0 | #107 <br> 11848/Dpa2wW <br> 11851/5vLrrt | | #96 <br> 11582/ESva9o <br> 11598/cbUBCA | #75 <br> 8885/RbQd0n <br> 8850/XQbTnh |

### Mapping of (characters, songs) to `objectName` edits

| | hski | ttmr | fktn | amao | kllj | kcna | ssmk | shro | hrnm | hume |
| - | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| all-003 | #27 <br> 6038/8tllfB <br> - | #29 <br> 6088/Rzwcaw <br> - | #25 <br> 6012/JZ8G1Y <br> - | #28 <br> 6039/oqiH3Q <br> - | #26 <br> 6022/COZKHv <br> - | #32 <br> 6199/XwlZOm <br> - | #30 <br> 6132/dO1J7J <br> - | #34 <br> 6266/2DroMz <br> - | #31 <br> 6145/3kcXWe <br> - | #33 <br> 6214/UMSszG <br> - |
| all-004 | #43 <br> 6441/Ks5tH0 <br> - | #41 <br> 6381/B9SnrG <br> - | #46 <br> 6589/9Wt6Gs <br> - | #39 <br> 6360/ctoDFI <br> - | #40 <br> 6372/zQHVoj <br> - | #44 <br> 6501/hYUgLC <br> - | #38 <br> 6353/s0Tnid <br> - | #45 <br> 6552/DwrrZf <br> - | #42 <br> 6439/Mf9rqI <br> - | #47 <br> 6591/DFwfpc <br> - |
| all-006 | #72 <br> - <br> 8862/GGjxnQ | #71 <br> - <br> 8901/ZPZVrx | | #69 <br> - <br> 8748/oW8UGV | | #70 <br> - <br> 8732/9hrq1V | #67 <br> - <br> 8674/XSf0oj | #73 <br> - <br> 8891/nv9JAf | #68 <br> - <br> 8704/aabOep | |
| char-002 | | | | | | #48 <br> - <br> 6648/yXR7hn | | #36 <br> 6309/kmS6W2 <br> - | | |
| char-003 | | | | | #35 <br> 6288/sZlsvv <br> - | | | | | |
