import GkmasObjectManager as gom
from GkmasObjectManager.const import GKMAS_OBJECT_SERVER

import json
from urllib.parse import urljoin


m = gom.fetch()
# m = gom.load("v199.json")
resourceList = []

# sud_music_general_all-001-amao_game.mp3 -> img_general_music_jacket_all-amao-001.png
# sud_music_general_ttmr-003-ttmr_game.mp3 -> img_general_music_jacket_char-ttmr-003.png

for obj in m.search(".*.mp3$"):

    segs = obj.name.split("-")
    songid_head = segs[0].split("_")[-1]
    songid_tail = segs[1]
    artist = segs[2].split("_")[0]
    songtype = "all" if songid_head == "all" else "char"

    resourceList.append(
        {
            "id": obj.id,
            "name": obj.name,
            "size": obj.size,
            "md5": obj.md5,
            "url": urljoin(GKMAS_OBJECT_SERVER, obj.objectName),
            "cover": urljoin(
                GKMAS_OBJECT_SERVER,
                m[
                    f"img_general_music_jacket_{songtype}-{artist}-{songid_tail}.png"
                ].objectName,
            ),
            "keywords": [f"{songid_head}-{songid_tail}", artist],
        }
    )

revision = m.revision._get_canon_repr()
resourceList = sorted(resourceList, key=lambda x: x["id"])
for i in range(len(resourceList)):
    resourceList[i]["id"] = i + 1  # switch to serial ID for compatibility with CRUD app

with open(f"manifest_v{revision}.json", "w") as f:
    json.dump(
        {
            "revision": m.revision._get_canon_repr(),
            "resourceList": resourceList,
        },
        f,
        indent=4,
    )
