function checkEmptyInputAndWarn(element) {
    if ($(element).val().trim() === "") {
        $(element).addClass("is-invalid");
        $(element).attr("placeholder", "Missing");
        $(element).focus();
        return false;
    } else {
        $(element).removeClass("is-invalid");
        return true;
    }
}

$(document).ready(function () {
    for (let keyword of info.keywords) {
        let alias = CHARACTER_ALIAS[keyword];
        if (alias) {
            setAccentColorByString(alias);
        }
    }

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
                <input type="text" class="fs-4 form-control me-2" placeholder="Keyword" />
                <button id="editorKeywordsDeleteButton" type="button" class="fs-4 btn btn-danger bi bi-trash"></button>
            </li>`
        );
    });

    // event delegation for dynamically added elements
    $(document).on("click", "#editorKeywordsDeleteButton", function () {
        $(this).parent().remove();
    });

    $("#editorSubmitButton").on("click", function () {
        if (
            !checkEmptyInputAndWarn("#editorFieldName") ||
            !checkEmptyInputAndWarn("#editorFieldSongUrl") ||
            !checkEmptyInputAndWarn("#editorFieldCoverUrl")
        )
            return;

        let keywords = [];
        $("#keywords-list-ul input").each(function () {
            if (checkEmptyInputAndWarn(this)) {
                keywords.push($(this).val());
            }
        });

        $.ajax({
            type: "POST",
            url: "/api/edit/" + info.id,
            contentType: "application/json",
            data: JSON.stringify({
                name: $("#editorFieldName").val(),
                url:
                    "https://object.asset.game-gakuen-idolmaster.jp/" +
                    $("#editorFieldSongUrl").val(),
                cover:
                    "https://object.asset.game-gakuen-idolmaster.jp/" +
                    $("#editorFieldCoverUrl").val(),
                keywords: keywords,
                caption: $("#editorCaption").val(),
            }),
            success: function () {
                window.location.href = "/view/" + info.id;
            },
            error: function (...args) {
                dumpErrorToConsole(...args);
            },
        });
    });
});
