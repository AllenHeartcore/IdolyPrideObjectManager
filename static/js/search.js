let searchResult = [];
let sortState = {
    byID: false,
    ascending: true,
}; // backend sorts by ascending name

function updateSortIcons() {
    if (sortState.byID) {
        $("#sortNameIcon").hide();
        $("#sortIDIcon").show();
        $("#sortIDIcon").removeClass("bi-caret-up-fill bi-caret-down-fill");
        if (sortState.ascending) {
            $("#sortIDIcon").addClass("bi-caret-up-fill");
        } else {
            $("#sortIDIcon").addClass("bi-caret-down-fill");
        }
    } else {
        $("#sortIDIcon").hide();
        $("#sortNameIcon").show();
        $("#sortNameIcon").removeClass("bi-caret-up-fill bi-caret-down-fill");
        if (sortState.ascending) {
            $("#sortNameIcon").addClass("bi-caret-up-fill");
        } else {
            $("#sortNameIcon").addClass("bi-caret-down-fill");
        }
    }
}

function buildResultTable(result) {
    updateSortIcons();
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

function sortAndBuildResultTable(comparator) {
    let sortedResult = searchResult.sort(comparator);
    if (!sortState.ascending) {
        sortedResult.reverse();
    }
    buildResultTable(sortedResult);
}

function populateSearchpageContainers(result) {
    if (result.length === 0) {
        $("#searchResultDigest").text("No results found.");
        return;
    }
    $("#searchResultDigest").text(`Found ${result.length} result(s).`);

    buildResultTable(result);

    $("#loadingSpinner").hide();
    $("#searchpageElements").show();
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
        if (sortState.byID) {
            sortState.ascending = !sortState.ascending;
        } else {
            sortState.byID = true;
            sortState.ascending = true;
        }

        sortAndBuildResultTable((a, b) => {
            // alphabetical order in entry.type implies AssetBundle < Resource
            if (a.type < b.type) return -1;
            if (a.type > b.type) return 1;
            return a.id - b.id;
        });
    });

    $("#sortName").click(function () {
        if (!sortState.byID) {
            sortState.ascending = !sortState.ascending;
        } else {
            sortState.byID = false;
            sortState.ascending = true;
        }

        sortAndBuildResultTable((a, b) => {
            return a.name.localeCompare(b.name);
        });
    });
});
