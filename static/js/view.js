function populateViewpageContainers(info) {
    $("#viewTitle").show();
    $("#viewTitle").text(info.id);
    $("#viewSubtitle").show();
    $("#viewSubtitle").text(info.name);

    $("#viewPropertyTable").show();
    $("#viewPropertyTable tbody").append(
        $("<tr>").append($("<th>").text("Size"), $("<td>").text(info.size)),
        info.crc
            ? $("<tr>").append($("<th>").text("CRC"), $("<td>").text(info.crc))
            : "", // very neat syntactic sugar
        $("<tr>").append($("<th>").text("MD5"), $("<td>").text(info.md5)),
        $("<tr>").append(
            $("<th>").text("Download Links"),
            $("<td>")
                .attr("id", "downloadLinks")
                .append(
                    $("<a>")
                        .attr(
                            "href",
                            `https://object.asset.game-gakuen-idolmaster.jp/${info.objectName}`
                        )
                        .attr("rel", "noopener noreferrer")
                        .text(`Raw ${type.toLowerCase()}`)
                )
        ),
        info.dependencies
            ? $("<tr>").append(
                  $("<th>").text("Dependencies"),
                  $("<td>")
                      .addClass("text-monospace")
                      .append(
                          $("<ul>").append(
                              info.dependencies.map((dep) =>
                                  $("<li>").append(
                                      $("<a>")
                                          .attr(
                                              "href",
                                              `/view/assetbundle/${dep.id}`
                                          )
                                          .text(dep.name)
                                  )
                              )
                          )
                      )
              )
            : ""
    );

    $("#viewMedia").show();
    getMedia(info.name.replace(/\.[^/.]+$/, ""));
    // info.name, with extension removed, is passed all the way to filename
    // in displayMedia and used to build the direct download link

    $("#viewCaption").show();
    getCaption();
}

function reportViewpageError() {
    $("#viewTitle").show();
    $("#viewTitle").html(`
        ${type} #${id} cannot be found, <br>
        or we encountered a parsing error. <br>
        Check console and Flask terminal. <br>
        Refresh to retry.
    `);
}

function getMedia(filename) {
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${id}/bytestream`,
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
        url: `/api/${type.toLowerCase()}/${id}/caption`,
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
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${id}`,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            populateViewpageContainers(result);
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
            reportViewpageError();
        },
    });
});
