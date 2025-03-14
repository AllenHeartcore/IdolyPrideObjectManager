function getCaption() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: `/api/${type.toLowerCase()}/${info.id}/caption`,
            dataType: "text",
            contentType: "charset=utf-8",
            success: function (caption) {
                resolve(caption);
            },
            error: function (...args) {
                dumpErrorToConsole(...args);
                reject("[An error occurred while generating caption.]");
            },
        });
    });
}

function displayCaption() {
    getCaption().then((caption) => {
        $("#loadingSpinnerCaption").hide();
        $("#viewCaptionText").show();
        $("#viewCaptionText").text(caption);
    });
}

$(document).ready(function () {
    for (let keyword of info.keywords) {
        let alias = CHARACTER_ALIAS[keyword];
        if (alias) {
            setAccentColorByString(alias);
        }
    }

    displayCaption();

    $("#editorFieldSongUrl").on("input", function () {
        let objectName = $(this).val();
        if (objectName === "") {
            $("#editorMediaAudio").attr("src", info.url);
        } else {
            $("#editorMediaAudio").attr(
                "src",
                "https://object.asset.game-gakuen-idolmaster.jp/" + objectName
            );
        }
    });

    $("#editorFieldCoverUrl").on("input", function () {
        let objectName = $(this).val();
        if (objectName === "") {
            $("#editorMediaImage").attr("src", info.cover);
        } else {
            $("#editorMediaImage").attr(
                "src",
                "https://object.asset.game-gakuen-idolmaster.jp/" + objectName
            );
        }
    });

    $("#editorMediaImage").on("error", function () {
        $(this).attr(
            "src",
            "data:image/svg+xml;charset=UTF-8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'><rect width='100%' height='100%' fill='%23cccccc'/></svg>"
        );
    });
});
