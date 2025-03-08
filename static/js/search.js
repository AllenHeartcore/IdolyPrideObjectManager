let searchResult = [];
let currentIDAscending = false;
let currentNameAscending = true;

function populateSearchpageContainers(result) {
    $("#loadingSpinner").hide();

    $("#searchQuery").show();
    $("#searchResultDigest").show();
    if (result.length === 0) {
        $("#searchResultDigest").text("No results found.");
        return;
    }
    $("#searchResultDigest").text(`Found ${result.length} result(s).`);

    $("#searchResultTable").show();
    populateSearchResultTable(result);
}

function populateSearchResultTable(result) {
    $("#searchResultTableBody").empty();
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

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: `/api/search/${query}`,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            searchResult = result;
            populateSearchpageContainers(searchResult);
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
        },
    });

    $("#sortID").click(function () {
        currentIDAscending = !currentIDAscending;
        let sortedResult = searchResult.sort((a, b) => {
            // alphabetical order in entry.type implies AssetBundle < Resource
            if (a.type < b.type) return -1;
            if (a.type > b.type) return 1;
            return a.id - b.id;
        });
        if (!currentIDAscending) {
            sortedResult.reverse();
        }
        populateSearchResultTable(sortedResult);
    });

    $("#sortName").click(function () {
        currentNameAscending = !currentNameAscending;
        let sortedResult = searchResult.sort((a, b) => {
            return a.name.localeCompare(b.name);
        });
        if (!currentNameAscending) {
            sortedResult.reverse();
        }
        populateSearchResultTable(sortedResult);
    });
});
