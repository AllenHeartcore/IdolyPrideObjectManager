import json
from sys import argv
from pathlib import Path


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


if __name__ == "__main__":

    p = Path(argv[1])
    manifest = json.loads(p.read_text())
    resourceList = []

    for res in manifest["resourceList"]:

        song_id, char_id = res["keywords"]
        title, release_date = song_map[song_id]
        char_jp, char_en = character_map[char_id]
        title += f" ({char_jp} ver.)" if song_id.startswith("all-") else ""

        resourceList.append(
            {
                "id": res["id"],
                "name": res["name"],
                "title": title,
                "size": res["size"],
                "md5": res["md5"],
                "url": res["url"],
                "cover": res["cover"],
                "keywords": [release_date, char_en],
            }
        )

    Path(p.stem + "_new.json").write_text(
        json.dumps(
            {
                "revision": manifest["revision"],
                "resourceList": resourceList,
            },
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
