const WALLPAPER_REGEX_PATTERN =
    /^img_general_(cidol.*thumb-landscape-large|(csprt|meishi_base).*full)$/;

function populateHomepageContainers(data) {
    $("#loadingSpinner").hide();

    $("#homeMetadata").show();
    $("#homeMetadataRevision").text(data.revision);
    $("#homeMetadataAbCount").text(data.assetBundleList.length);
    $("#homeMetadataResCount").text(data.resourceList.length);

    let matches = data.assetBundleList
        .filter((ab) => WALLPAPER_REGEX_PATTERN.test(ab.name))
        .map((ab) => ({ id: ab.id, name: ab.name }));

    $("#homeDigest").show();
    let latestSamples = matches.sort((a, b) => a.id - b.id).slice(-5);
    latestSamples.forEach((item) => {
        $("#homeDigestList").append(
            $("<li>").append(
                $("<a>")
                    .attr("href", `/view/assetbundle/${item.id}`)
                    .text(item.name)
            )
        );
    });
}

function reportHomepageError() {
    $("#loadingSpinner").hide();
    $("#homeMetadata").show();
    $("#homeMetadata").html(`
        GkmasManifest cannot be fetched. <br>
        Check Internet connection. <br>
        Refresh to retry.
    `);
}

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/api/manifest",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            populateHomepageContainers(result);
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
            reportHomepageError();
        },
    });
});
