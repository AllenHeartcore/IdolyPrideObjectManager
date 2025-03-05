function populateSearchResult(result) {
    $("#loadingSpinner").hide();

    $("#searchQuery").show();
    $("#searchResultDigest").show();
    if (result.length === 0) {
        $("#searchResultDigest").text("No results found.");
        return;
    }
    $("#searchResultDigest").text(`Found ${result.length} result(s).`);

    $("#searchResultTable").show();
    result.forEach((entry) => {
        $("#searchResultTable").append(
            $("<tr>").append(
                $("<td>").text(`${entry.type} #${entry.id}`),
                $("<td>").append(
                    $("<a>")
                        .attr(
                            "href",
                            `/view/${entry.type.toLowerCase()}/${entry.id}`
                        )
                        .text(entry.name)
                )
            )
        );
    });
}

function reportSearchError() {}

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: `/api/search/${query}`,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            populateSearchResult(result);
        },
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
            reportSearchError();
        },
    });
});
