const WALLPAPER_REGEX_PATTERN = /img_general_(cidol|csprt|meishi_base).*full.*/;

function populateHomepageContainers(data) {
    $("#loadingSpinner").hide();

    $("#homeMetadata").show();
    $("#homeMetadataRevision").text(data.revision);
    $("#homeMetadataAbCount").text(data.assetBundleList.length);
    $("#homeMetadataResCount").text(data.resourceList.length);

    // for each asset bundle, check if matches the wallpaper regex
    // if it does, add it to the carousel

    // matches is empty list
    // let matches = [];
    // data.assetBundleList.forEach((ab) => {
    //     if (WALLPAPER_REGEX_PATTERN.test(ab.name)) {
    //         matches.push(ab.name);
    //     }
    // });
    let matches = data.assetBundleList
        .filter((ab) => WALLPAPER_REGEX_PATTERN.test(ab.name))
        .map((ab) => ab.name);
    console.log(matches);
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
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
            $("#loadingSpinner").hide();
        },
    });
});
