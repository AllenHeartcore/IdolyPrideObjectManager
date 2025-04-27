const MEDIA_ALIAS = {
    "img": "Image",
    "sud": "Audio",
    "mov": "Video",
    "adv": "Story",
    "mdl": "Model",
    "mot": "Motion",
    "env": "Environment",
    "eff": "Effect",
};

const SUBTYPE_ALIAS = {
    "img card full_0": "Idol Img",
    "img card full_1": "Idol Card",
    "img cos thumb": "Costume",
    "img photo full": "Photo",
    "img story": "Storycard",
    "img deco": "Decoration",
    "img ui diary": "Diary",
    "img acc": "Skillcard",
    "sud music short": "Songs",
    "sud bgm": "BGM",
    "mov card 1080p": "Animation",
    "mov mv 1080p": "MV",
};

const CHARACTER_ALIAS = {
    "ktn": "Nagase Kotono",
    "ngs": "Ibuki Nagisa",
    "ski": "Shiraishi Saki",
    "suz": "Narumiya Suzu",
    "mei": "Hayasaka Mei",
    "skr": "Kawasaki Sakura",
    "szk": "Hyodo Shizuku",
    "chs": "Shiraishi Chisa",
    "rei": "Ichinose Rei",
    "hrk": "Saeki Haruko",
    "rui": "Tendo Rui",
    "yu": "Suzumura Yu",
    "smr": "Okuyama Sumire",
    "rio": "Kanzaki Rio",
    "aoi": "Igawa Aoi",
    "ai": "Komiyama Ai",
    "kkr": "Akazaki Kokoro",
    "mna": "Nagase Mana",
    "kor": "Yamada Kaori",
    "kan": "Kojima Kana",
    "mhk": "Takeda Mihoko",
};

function dumpErrorToConsole(...args) {
    var name_of_parent_function = arguments.callee.caller.name;
    console.error("Error in " + name_of_parent_function);
    args.forEach((arg) => {
        console.error(arg);
    });
}

function getMediaBlobURL(type, id) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: `/api/${type.toLowerCase()}/${id}/bytestream`,
            xhrFields: { responseType: "arraybuffer" },
            success: function (data, status, request) {
                const mimetype = request.getResponseHeader("Content-Type");
                blob = new Blob([data], { type: mimetype });
                resolve({
                    url: URL.createObjectURL(blob),
                    mimetype: mimetype,
                });
            },
            error: function (...args) {
                dumpErrorToConsole(...args);
                blob = new Blob(["An error occurred while fetching media."], {
                    type: "text/plain",
                });
                reject({
                    url: URL.createObjectURL(blob),
                    mimetype: "text/plain",
                });
            },
        });
    });
}
