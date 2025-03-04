$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/api/manifest",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            $("#loadingSpinner").hide();
            $("#homeMetadata").show();
            $("#homeMetadataRevision").text(result.revision);
            $("#homeMetadataAbCount").text(result.assetBundleList.length);
            $("#homeMetadataResCount").text(result.resourceList.length);
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
