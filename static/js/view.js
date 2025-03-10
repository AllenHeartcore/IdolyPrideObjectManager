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
            container.append(
                $("<a>")
                    .attr("href", url)
                    .text("Download Media")
                    .attr("download", "")
            );
        }

        $("#downloadLinks").append(
            "&emsp; | &emsp;",
            $("<a>")
                .attr("href", url)
                .attr("download", info.name.replace(/\.[^/.]+$/, ""))
                .text("Converted media")
        );
    });
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
