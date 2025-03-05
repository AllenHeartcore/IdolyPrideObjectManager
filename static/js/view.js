// general-purpose base64 media viewer
function buildViewpageEmbeddedMedia() {
    let base64Url = $("#viewEmbeddedMedia").attr("data-src");
    if (!base64Url) return;
    console.log(base64Url);

    let mimeType = base64Url.match(/^data:([^;]+);base64,/);
    if (!mimeType) return;

    let type = mimeType[1].split("/")[0];
    let $embedElement;

    switch (type) {
        case "image":
            $embedElement = $("<img>").attr("src", base64Url);
            $embedElement.attr("id", "viewImageResponsive");
            break;
        case "audio":
            $embedElement = $("<audio>").attr({
                src: base64Url,
                controls: true,
            });
            break;
        case "video":
            $embedElement = $("<video>").attr({
                src: base64Url,
                controls: true,
            });
            break;
        case "text":
            $embedElement = $("<iframe>").attr({
                src: base64Url,
            });
            break;
        default:
            $embedElement = $("<span>").text("Unsupported Base64 content");
    }

    $("#viewEmbeddedMedia").append($embedElement);
}

function populateViewpageContainers(info) {
    $("#loadingSpinner").hide();

    $("#viewTitle").show();
    $("#viewTitle").text(info.id);
    $("#viewSubtitle").show();
    $("#viewSubtitle").text(info.name);

    $("viewEmbeddedMedia").show();
    $("#viewEmbeddedMedia").attr("data-src", info.embed_url);
    buildViewpageEmbeddedMedia();

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

function displayCaption(text) {
    $("#loadingSpinnerCaption").hide();
    $("#viewCaptionText").show();
    $("#viewCaptionText").text(text);
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
