function populateViewpageContainers(info) {
    $("#loadingSpinner").hide();

    $("#viewTitle").show();
    $("#viewTitle").text(info.id);
    $("#viewSubtitle").show();
    $("#viewSubtitle").text(info.name);
    $("viewImageResponsive").show();
    $("#viewImageResponsive").attr("src", info.embed_url);

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
                    .text(`Raw ${type}`),
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
}

$(document).ready(function () {
    console.log("Querying API for view page data...");
    console.log("URL is: " + `/api/${type}/${id}`);
    $.ajax({
        type: "GET",
        url: `/api/${type}/${id}`,
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
            $("#loadingSpinner").hide();
        },
    });
});
