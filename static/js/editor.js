let isAudioLoaded = true;
let isImageLoaded = true;

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

function checkInvalidMediaAndWarn(element, flag) {
    if (flag) {
        $(element).addClass("is-invalid");
        $(element).attr("placeholder", "Invalid");
        $(element).focus();
        return false;
    } else {
        $(element).removeClass("is-invalid");
        return true;
    }
}

// all the hassle is here for a reason...
function updateImage(url) {
    var imgBuffer = new Image();

    imgBuffer.onload = function () {
        $("#editorMediaImage").attr("src", url);
        isImageLoaded = true;
    };

    imgBuffer.onerror = function () {
        $("#editorMediaImage").attr(
            "src",
            "data:image/svg+xml;charset=UTF-8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%'><rect width='100%' height='100%' fill='%23dddddd'/></svg>"
        );
        isImageLoaded = false;
        // Without the buffer, the action of loading the placeholder itself
        // will trigger the onload event, therefore the flag is never set to false!
        // Therefore the buffer serves a "3rd-party auditor" that handles all events.
    };

    imgBuffer.src = url; // start loading
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
        updateImage(
            "https://object.asset.game-gakuen-idolmaster.jp/" + $(this).val()
        );
    });

    $("#editorMediaAudio").on("loadeddata", function () {
        console.log("Audio loaded");
        isAudioLoaded = true;
    });

    $("#editorMediaAudio").on("error", function () {
        console.log("Audio error");
        isAudioLoaded = false;
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
            !checkEmptyInputAndWarn("#editorFieldCoverUrl") ||
            !checkInvalidMediaAndWarn("#editorFieldSongUrl", !isAudioLoaded) ||
            !checkInvalidMediaAndWarn("#editorFieldCoverUrl", !isImageLoaded)
        )
            return;

        let keywords = [];
        let isKeywordsValid = true;
        $("#keywords-list-ul input").each(function () {
            if (checkEmptyInputAndWarn(this)) {
                keywords.push($(this).val());
            } else {
                isKeywordsValid = false;
                return; // this only breaks the loop but **stays in the function**
            }
        });
        if (!isKeywordsValid) return;

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
