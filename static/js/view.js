function getMedia(filename) {
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${info.id}/bytestream`,
        xhrFields: { responseType: "arraybuffer" },
        success: function (data, status, request) {
            const mimetype = request.getResponseHeader("Content-Type");
            displayMedia(data, mimetype, filename);
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
            displayMedia(
                "text/plain",
                "An error occurred while fetching media.",
                filename
            );
        },
    });
}

function displayMedia(data, mimetype, filename) {
    $("#loadingSpinnerMedia").hide();
    $("#viewMediaContent").show();
    let container = $("#viewMediaContent");

    const blob = new Blob([data], { type: mimetype });
    const url = URL.createObjectURL(blob);

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
            .attr("download", filename)
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
            displayCaption(caption);
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
            displayCaption("[An error occurred while generating caption.]");
        },
    });
}

function displayCaption(text) {
    $("#loadingSpinnerCaption").hide();
    $("#viewCaptionText").show();
    $("#viewCaptionText").text(text);
}

$(document).ready(function () {
    setAccentColorByString(info.name);

    // info.name, with extension removed, is passed all the way to filename
    // in displayMedia and used to build the direct download link
    getMedia(info.name.replace(/\.[^/.]+$/, ""));
    getCaption();
});
