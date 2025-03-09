function displayMedia() {
    $("#loadingSpinnerMedia").hide();
    $("#viewMediaContent").show();
    let container = $("#viewMediaContent");

    const blob = getMediaBlob(type, info.id);
    const url = URL.createObjectURL(blob);
    const mimetype = blob.type;

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
}

function getCaption() {
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${info.id}/caption`,
        dataType: "text",
        contentType: "charset=utf-8",
        success: function (caption) {
            return caption;
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
            return "[An error occurred while generating caption.]";
        },
    });
}

function displayCaption() {
    let caption = getCaption();
    $("#loadingSpinnerCaption").hide();
    $("#viewCaptionText").show();
    $("#viewCaptionText").text(caption);
}

$(document).ready(function () {
    setAccentColorByString(info.name);

    displayMedia();
    getCaption();
});
