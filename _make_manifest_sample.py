import GkmasObjectManager as gom
from GkmasObjectManager.const import GKMAS_OBJECT_SERVER

import json
from urllib.parse import urljoin


song_map = {
    "all-001": ("初", "May 2024"),
    "all-002": ("Campus mode!!", "June 2024"),
    "all-003": ("キミとセミブルー", "July 2024"),
    "all-004": ("冠菊", "August 2024"),
    "all-005": ("仮装狂騒曲", "October 2024"),
    "all-006": ("White Night! White Wish!", "December 2024"),
    "all-007": ("ハッピーミルフィーユ", "February 2025"),
    "all-008": ("古今東西ちょちょいのちょい", "November 2024"),
    "all-009": ("雪解けに", "March 2025"),
    "hski-001": ("Fighting My Way", "May 2024"),
    "hski-002": ("Boom Boom Pow", "June 2024"),
    "ttmr-001": ("Luna say maybe", "May 2024"),
    "ttmr-002": ("アイヴイ", "May 2024"),
    "ttmr-003": ("叶えたい、ことばかり", "June 2024"),
    "fktn-001": ("世界一可愛い私", "May 2024"),
    "fktn-002": ("Yellow Big Bang!", "June 2024"),
    "hrnm-001": ("clumsy trick", "May 2024"),
    "hrnm-002": ("L.U.V", "October 2024"),
    "hrnm-003": ("marble heart", "March 2025"),
    "ssmk-001": ("Tame-Lie-One-Step", "May 2024"),
    "ssmk-002": ("カクシタワタシ", "December 2024"),
    "ssmk-003": ("Ride on Beat", "November 2024"),
    "shro-001": ("光景", "May 2024"),
    "shro-002": ("コントラスト", "July 2024"),
    "shro-003": ("メクルメ", "December 2024"),
    "kllj-001": ("白線", "May 2024"),
    "kllj-003": ("Wake up!!", "July 2024"),
    "kcna-001": ("Wonder Scale", "May 2024"),
    "kcna-002": ("日々、発見的ステップ！", "August 2024"),
    "kcna-003": ("憧れをいっぱい", "August 2024"),
    "amao-001": ("Fluorite", "May 2024"),
    "amao-002": ("Feel Jewel Dream", "September 2024"),
    "amao-003": ("Sweet Magic", "January 2025"),
    "hume-001": ("The Rolling Riceball", "June 2024"),
    "hmsz-001": ("ツキノカメ", "February 2025"),
    "hmsz-003": ("たいせつなもの", "February 2025"),
    "jsna-001": ("小さな野望", "November 2024"),
    "jsna-003": ("Cosmetic", "December 2024"),
}

character_map = {
    "hski": ("花海 咲季", "Hanami Saki"),
    "ttmr": ("月村 手毬", "Tsukimura Temari"),
    "fktn": ("藤田 ことね", "Fujita Kotone"),
    "amao": ("有村 麻央", "Arimura Mao"),
    "kllj": ("葛城 リーリヤ", "Katsuragi Lilja"),
    "kcna": ("倉本 千奈", "Kuramoto China"),
    "ssmk": ("紫雲 清夏", "Shiun Sumika"),
    "shro": ("篠澤 広", "Shinosawa Hiro"),
    "hrnm": ("姫崎 莉波", "Himesaki Rinami"),
    "hume": ("花海 佑芽", "Hanami Ume"),
    "hmsz": ("秦谷 美鈴", "Hataya Misuzu"),
    "jsna": ("十王 星南", "Juo Sena"),
}

single_map = {
    "001": "1st Single",
    "002": "2nd Single",
    "003": "Birthday Single",
}


m = gom.fetch()
# m = gom.load("v199.json")
resourceList = []

# sud_music_general_all-001-amao_game.mp3 -> img_general_music_jacket_all-amao-001.png
# sud_music_general_ttmr-003-ttmr_game.mp3 -> img_general_music_jacket_char-ttmr-003.png

for obj in m.search(".*.mp3$"):

    segs = obj.name.split("-")

    songid_head = segs[0].split("_")[-1]
    songid_tail = segs[1]
    songid = f"{songid_head}-{songid_tail}"
    title, release_date = song_map[songid]

    charid = segs[2].split("_")[0]
    char_jp, char_en = character_map[charid]

    if songid_head == "all":
        songtype = "all"
        title += f" ({character_map[charid][0]} ver.)"
        single_flag = ""
    else:
        songtype = "char"
        single_flag = single_map[songid_tail]

    resourceList.append(
        {
            "id": obj.id,
            "name": title,
            "size": obj.size,
            "md5": obj.md5,
            "url": urljoin(GKMAS_OBJECT_SERVER, obj.objectName),
            "cover": urljoin(
                GKMAS_OBJECT_SERVER,
                m[
                    f"img_general_music_jacket_{songtype}-{charid}-{songid_tail}.png"
                ].objectName,
            ),
            "keywords": [release_date, char_en],
        }
    )

    if single_flag:
        resourceList[-1]["keywords"].append(single_flag)

revision = m.revision._get_canon_repr()
resourceList = sorted(resourceList, key=lambda x: x["id"])
for i in range(len(resourceList)):
    resourceList[i]["id"] = i + 1  # switch to serial ID for compatibility with CRUD app

with open(f"manifest_v{revision}.json", "w", encoding="utf-8") as f:
    json.dump(
        {
            "revision": m.revision._get_canon_repr(),
            "resourceList": resourceList,
        },
        f,
        indent=4,
        ensure_ascii=False,
    )
