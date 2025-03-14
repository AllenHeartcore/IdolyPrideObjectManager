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
        let url =
            "https://object.asset.game-gakuen-idolmaster.jp/" + $(this).val();
        $("#editorMediaAudio").attr("src", url);

        if ($(this).val() !== info.url.slice(-6)) {
            $("#editorTableSize").text("Changed");
            $("#editorTableMD5").text("Changed");
        } else {
            $("#editorTableSize").text(info.size);
            $("#editorTableMD5").text(info.md5);
        }
    });

    $("#editorFieldCoverUrl").on("input", function () {
        let url =
            "https://object.asset.game-gakuen-idolmaster.jp/" + $(this).val();
        $("#editorMediaImage").attr("src", url);
    });

    // gray rectangle filler for invalid url
    $("#editorMediaImage").on("error", function () {
        $(this).attr(
            "src",
            "data:image/svg+xml;charset=UTF-8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'><rect width='100%' height='100%' fill='%23dddddd'/></svg>"
        );
    });

    $("#editorKeywordsAddButton").on("click", function () {
        $("#keywords-list-ul").append(
            `<li class="mb-2 d-flex">
                <input type="text" class="fs-4 form-control me-2" />
                <button id="editorKeywordsDeleteButton" type="button" class="fs-4 btn btn-danger bi bi-trash"></button>
            </li>`
        );
    });

    // event delegation for dynamically added elements
    $(document).on("click", "#editorKeywordsDeleteButton", function () {
        $(this).parent().remove();
    });
});
