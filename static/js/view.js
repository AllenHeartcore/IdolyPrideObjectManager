function populateViewpageContainers(info) {
    $("#loadingSpinner").hide();

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
            $("<td>").append(
                $("<a>")
                    .attr(
                        "href",
                        `https://object.asset.game-gakuen-idolmaster.jp/${info.objectName}`
                    )
                    .attr("rel", "noopener noreferrer")
                    .text(`Raw ${type.toLowerCase()}`),
                info.embed_url
                    ? [
                          "&emsp; | &emsp;",
                          $("<a>")
                              .attr("href", info.embed_url)
                              .attr("download", info.name) // specify download name
                              .text("Extracted media"),
                      ]
                    : ""
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
    getMedia(info.mimetype);

    $("#viewCaption").show();
    getCaption();
}

function reportViewpageError() {
    $("#loadingSpinner").hide();
    $("#viewTitle").show();
    $("#viewTitle").html(`
        ${type} #${id} cannot be found, <br>
        or we encountered a parsing error. <br>
        Check console and Flask terminal. <br>
        Refresh to retry.
    `);
}

function getMedia(mimetype) {
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${id}/bytestream`,
        xhrFields: { responseType: "arraybuffer" },
        success: function (data, status, request) {
            const mimetype = request.getResponseHeader("Content-Type");
            displayMedia(data, mimetype);
        },
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
            displayMedia(
                "text/plain",
                "An error occurred while fetching media."
            );
        },
    });
}

function displayMedia(data, mimetype) {
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
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
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
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
            reportViewpageError();
        },
    });
});
