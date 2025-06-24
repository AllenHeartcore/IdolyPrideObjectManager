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

/*
    The two drivers below expect a rigid class structure in the container:
        media-container  (handled by progressedMediaDriver)
        - prog-container (handled by progressDriver)
        - - prog-stage
        - - prog-num
        - - prog-bar-container
        - - - prog-bar
        - media-content
*/

function progressedMediaDriver(type, id, container, mediaPopulator) {
    const progress = container.find(".prog-container");
    const media = container.find(".media-content");
    let sse_src = progressDriver(type, id, progress, media);
    getMediaBlobURL(type, id)
        .then(({ url, mimetype, mtime }) => {
            sse_src.close();
            progress.hide();
            media.show();
            mediaPopulator(media, url, mimetype, mtime);
        })
        .catch((error) => {
            sse_src.close();
            progress.hide();
            media.show();
            media.text("Failed to load media: " + error.message);
            dumpErrorToConsole(error);
        });
}

function progressDriver(type, id, progress, media) {
    const src = new EventSource(`/sse/${type.toLowerCase()}/${id}/progress`);

    src.onopen = function () {
        progress.show();
        media.hide();
    };

    src.onerror = function (event) {
        progress
            .find(".prog-stage")
            .text("ERROR: Cannot subscribe to progress stream");
        progress.find(".prog-num").text("");
        progress.find(".prog-bar-container").hide();
        dumpErrorToConsole(event);
        src.close();
    };

    src.onmessage = function (event) {
        const data = JSON.parse(event.data);
        progress.find(".prog-stage").text(data.stage + "...");
        progress.find(".prog-num").text(data.completed + " / " + data.total);
        progress
            .find(".prog-bar")
            .css("width", (data.completed / data.total) * 100 + "%");
    };

    src.addEventListener("success", function (event) {
        const data = JSON.parse(event.data);
        progress.find(".prog-stage").text(data.message);
        progress.find(".prog-num").text("");
        progress.find(".prog-bar").css("width", "100%");
        src.close();
    });

    src.addEventListener("warning", function (event) {
        const data = JSON.parse(event.data);
        progress.find(".prog-stage").text("WARNING: " + data.message);
        console.warn(data.message);
    });

    src.addEventListener("error", function (event) {
        const data = JSON.parse(event.data);
        progress.find(".prog-stage").text("ERROR: " + data.message);
        progress.find(".prog-num").text("");
        progress.find(".prog-bar-container").hide();
        dumpErrorToConsole(event);
        src.close();
    });

    return src; // for external access
}

function getMediaBlobURL(type, id) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: `/api/${type.toLowerCase()}/${id}/bytestream`,
            xhrFields: { responseType: "arraybuffer" },

            success: function (data, status, request) {
                const mimetype = request.getResponseHeader("Content-Type");
                const mtime = request.getResponseHeader("Last-Modified");
                blob = new Blob([data], { type: mimetype });
                resolve({
                    url: URL.createObjectURL(blob),
                    mimetype: mimetype,
                    mtime: mtime.replace(/ GMT.*/, ""),
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
                    mtime: "Unknown",
                });
            },
        });
    });
}
