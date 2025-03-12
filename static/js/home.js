const NUM_FEATURED_SAMPLES = 12;

function populateHomepageContainers(data) {
    $("#homeMetadataRevision").text(data.revision);
    $("#homeMetadataResCount").text(data.resourceList.length);

    let latestSamples = data.resourceList
        .sort((a, b) => b.id - a.id)
        .slice(0, NUM_FEATURED_SAMPLES);

    latestSamples.forEach((item, index) => {
        let image = $("<img>")
            .attr("src", item.cover)
            .attr("alt", item.name)
            .addClass("image-roundedge shadow-at-hover");
        let link = $("<a>").attr("href", `/view/${item.id}`).append(image);
        $("#homeFeaturedContainer").append(
            $("<div>").addClass("col-md-2 mt-4").append(link)
        );
    });

    $("#loadingSpinner").hide();
    $("#homepageElements").show();
}

function reportHomepageError() {
    $("#loadingSpinner").hide();
    $("#homeMetadata").html(`
        GkmasManifest cannot be loaded. <br>
        manifest.json may be missing or corrupted. <br>
        Refresh to retry.
    `);
}

$(document).ready(function () {
    $("#navbarNav").children("#searchForm").remove();

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

    $("#homeGotoForm").submit(function (event) {
        event.preventDefault();
        let id = $("#homeGotoInput").val();
        let type = $("#homeGotoType").val();
        window.location.href = `/view/${id}`;
    });

    $("#homeGotoInput").keydown(function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#homeGotoForm").submit();
        }
    });
});
