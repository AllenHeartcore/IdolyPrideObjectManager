function displayMedia() {
    getMediaBlobURL(type, info.id).then(({ url, mimetype }) => {
        $("#loadingSpinnerMedia").hide();
        $("#viewMediaContent").show();
        let container = $("#viewMediaContent");

        if (mimetype.startsWith("image/")) {
            container.append($("<img>").attr("src", url));
        } else if (mimetype.startsWith("audio/")) {
            container.append($("<audio>").attr({ src: url, controls: true }));
        } else if (mimetype.startsWith("video/")) {
            container.append($("<video>").attr({ src: url, controls: true }));
        } else {
            handleUnsupportedMedia(url);
            return;
        }

        $("#downloadConvertedMedia")
            .text("Download Converted " + mimetype.split("/")[1].toUpperCase())
            .attr("href", url)
            .attr("download", info.name.replace(/\.[^/.]+$/, ""))
            .removeClass("disabled");
    });
}

function handleUnsupportedMedia(url) {
    $("#viewMediaContent").append(
        $("<div>").text("Preview not available for this type of media.")
    );
    if (type === "AssetBundle") {
        $("#downloadConvertedMedia")
            .text("Deobfuscated AssetBundle")
            .attr("href", url)
            .attr("download", info.name.replace(/\.[^/.]+$/, "") + ".unity3d")
            .removeClass("disabled");
    } else {
        $("#downloadConvertedMedia")
            .text("Conversion Unavailable")
            .removeClass("btn-primary")
            .addClass("btn-secondary");
    }
}

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
    setAccentColorByString(info.name);

    displayMedia();
    displayCaption();
});
