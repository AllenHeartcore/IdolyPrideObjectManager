const WALLPAPER_REGEX_PATTERN =
    /^img_general_(cidol.*thumb-landscape-large|(csprt|meishi_base).*full)$/;

function populateHomepageContainers(data) {
    $("#homeMetadataRevision").text(data.revision);
    $("#homeMetadataAbCount").text(data.assetBundleList.length);
    $("#homeMetadataResCount").text(data.resourceList.length);

    let matches = data.assetBundleList
        .filter((ab) => WALLPAPER_REGEX_PATTERN.test(ab.name))
        .map((ab) => ({ id: ab.id, name: ab.name }));

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

    $("#loadingSpinner").hide();
    $("#homepageElements").show();
}

function reportHomepageError() {
    $("#loadingSpinner").hide();
    $("#homeMetadata").html(`
        GkmasManifest cannot be fetched. <br>
        Check Internet connection. <br>
        Refresh to retry.
    `);
}

$(document).ready(function () {
    $("#navbarSearchForm").hide();
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

    $("#homeSearchForm").submit(function (event) {
        event.preventDefault();
        let query = $("#homeSearchInput").val();
        if (!query.trim()) {
            $("#homeSearchInput").val("");
            $("#homeSearchInput").focus();
            return;
        }
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
    });

    $("#homeSearchInput").keydown(function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#homeSearchForm").submit();
        }
    });
});
