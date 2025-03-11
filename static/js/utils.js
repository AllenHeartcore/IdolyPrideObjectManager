const MEDIA_ALIAS = {
    "img": "Image",
    "sud": "Audio",
    "mov": "Video",
    "adv": "Story",
    "mdl": "Model",
    "mot": "Motion",
    "env": "Environment",
    "fbx": "FBX",
};

const CHARACTER_ALIAS = {
    "hski": "Hanami Saki",
    "ttmr": "Tsukimura Temari",
    "fktn": "Fujita Kotone",
    "amao": "Arimura Mao",
    "kllj": "Katsuragi Lilja",
    "kcna": "Kuramoto China",
    "ssmk": "Shiun Sumika",
    "shro": "Shinosawa Hiro",
    "hrnm": "Himesaki Rinami",
    "hume": "Hanami Ume",
    "hmsz": "Hataya Misuzu",
    "jsna": "Juo Sena",
};

function dumpErrorToConsole(...args) {
    var name_of_parent_function = arguments.callee.caller.name;
    console.log("Error in " + name_of_parent_function);
    args.forEach((arg) => {
        console.log(arg);
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
