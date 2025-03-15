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
        $(element).val("");
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
        $("#editorMediaImage").attr("src", GRAY_RECTANGLE_PLACEHOLDER);
        isImageLoaded = false;
        // Without the buffer, the action of loading the placeholder itself
        // will trigger the onload event, therefore the flag is never set to false!
        // Therefore the buffer serves a "3rd-party auditor" that handles all events.
    };

    imgBuffer.src = url; // start loading
}

function showNotification() {
    const banner = $("#editorNotifBanner");
    banner.css("display", "block");
    banner.css("opacity", "1");
    setTimeout(() => {
        banner.css("opacity", "0");
        setTimeout(() => {
            banner.css("display", "none");
        }, 5000); // fade out
    }, 10); // start immediately
}

function resetContainers() {
    $("#editorID").text(info.id);
    $("#editorFieldName").val("");
    $("#editorFieldSongUrl").val("");
    $("#editorFieldCoverUrl").val("");
    $("#editorKeywordsList").empty();
    $("#editorCaption").val("");
    $("#editorMediaImage").attr("src", GRAY_RECTANGLE_PLACEHOLDER);
    $("#editorMediaAudio").attr("src", "");
    $("#editorTableSize").text("");
    $("#editorTableMD5").text("");
}

$(document).ready(function () {
    for (let keyword of info.keywords) {
        let alias = CHARACTER_ALIAS[keyword];
        if (alias) {
            setAccentColorByString(alias);
        }
    }

    if (!edit_mode) {
        $("#editorMediaImage").attr("src", GRAY_RECTANGLE_PLACEHOLDER);
        isAudioLoaded = false;
        isImageLoaded = false;
    }

    // <textarea> doesn't like indentations...
    caption = $("#editorCaption").val();
    $("#editorCaption").val(caption.trim());

    // Event listeners for media preview

    $("#editorFieldSongUrl").on("input", function () {
        let url = GKMAS_OBJECT_SERVER + $(this).val();
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
        updateImage(GKMAS_OBJECT_SERVER + $(this).val());
    });

    $("#editorMediaAudio").on("loadeddata", function () {
        isAudioLoaded = true;
    });

    $("#editorMediaAudio").on("error", function () {
        isAudioLoaded = false;
    });

    // Event listeners for buttons

    $("#editorKeywordsAddButton").on("click", function () {
        $("#editorKeywordsList").append(
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
        $("#editorKeywordsList input").each(function () {
            if (checkEmptyInputAndWarn(this)) {
                keywords.push($(this).val().trim());
            } else {
                isKeywordsValid = false;
                return; // this only breaks the loop but **stays in the function**
            }
        });
        if (!isKeywordsValid) return;

        $.ajax({
            type: "POST",
            url: "/api/update/" + info.id,
            contentType: "application/json",
            data: JSON.stringify({
                id: info.id,
                name: $("#editorFieldName").val().trim(),
                url: GKMAS_OBJECT_SERVER + $("#editorFieldSongUrl").val(),
                cover: GKMAS_OBJECT_SERVER + $("#editorFieldCoverUrl").val(),
                keywords: keywords,
                caption: $("#editorCaption").val().trim(),
            }),
            success: function () {
                if (edit_mode) {
                    window.location.href = "/view/" + info.id;
                } else {
                    $("#editorNotifID").text(info.id);
                    $("#editorNotifUrl").attr("href", "/view/" + info.id);
                    showNotification();
                    info.id = info.id + 1;
                    resetContainers();
                }
            },
            error: function (...args) {
                dumpErrorToConsole(...args);
            },
        });
    });

    $("#editorDiscardButton").on("click", function () {
        if (!confirm("Are you sure you want to discard your changes?")) {
            return;
        }
        if (edit_mode) {
            window.location.href = "/view/" + info.id;
        } else {
            resetContainers();
        }
    });
});
