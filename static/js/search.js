// We keep these vars global to avoid passing them around
let searchEntries = []; // this can be huge (up to ~10k entries)
let sortState = {
    byID: false,
    ascending: true,
}; // backend sorts by ascending name

function populateCardContainer() {
    $("#searchEntryCardContainer").empty();
    searchEntries.forEach((entry) => {
        let card = $("<div>").addClass("card").attr("id", "searchEntryCard");
        if (entry.name.startsWith("img_")) {
            getMediaBlobURL(entry.type, entry.id).then(({ url, mimetype }) => {
                card.prepend(
                    $("<img>")
                        .addClass("card-img-top")
                        .attr("id", "searchEntryCardImage")
                        .attr("src", url)
                        .attr("alt", entry.name)
                );
            });
        }
        let cardBody = $("<div>")
            .addClass("card-body")
            .append(
                $("<h5>").addClass("fs-3").text(`${entry.type} #${entry.id}`),
                $("<p>").addClass("fs-6 lh-1").text(entry.name)
            );
        card.append(cardBody);
        card.click(function () {
            window.location.href = `/view/${entry.type.toLowerCase()}/${
                entry.id
            }`;
        });
        $("#searchEntryCardContainer").append(
            $("<div>").addClass("col-md-3").append(card)
        );
    });
}

function sortSearchEntries() {
    if (sortState.byID) {
        searchEntries.sort((a, b) => {
            // alphabetical order in entry.type implies AssetBundle < Resource
            if (a.type < b.type) return -1;
            if (a.type > b.type) return 1;
            return a.id - b.id;
        });
    } else {
        searchEntries.sort((a, b) => {
            return a.name.localeCompare(b.name);
        });
    }
    if (!sortState.ascending) {
        searchEntries.reverse();
    }
}

function updateSort() {
    let byID_new = $("#sortByID").is(":checked");
    let ascending_new = $("#sortAsc").is(":checked");
    console.log(byID_new, ascending_new);
    if (byID_new === sortState.byID && ascending_new === sortState.ascending) {
        return;
    }
    sortState.byID = byID_new;
    sortState.ascending = ascending_new;
    sortSearchEntries();
    populateCardContainer();
}

function populateSearchpageContainers() {
    if (searchEntries.length === 0) {
        $("#searchResultDigest").text("No results found.");
    } else {
        $("#searchResultDigest").text(
            `Found ${searchEntries.length}` +
                (searchEntries.length === 1 ? " entry." : " entries.")
        );
        populateCardContainer();
    }

    $("#loadingSpinner").hide();
    $("#searchpageElements").show();
}

$(document).ready(function () {
    $("#searchInput").val(query); // allows immediate edit/resubmission

    $.ajax({
        type: "GET",
        url: `/api/search`,
        data: { query: query },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            searchEntries = result;
            populateSearchpageContainers();
        },
        error: function (...args) {
            dumpErrorToConsole(...args);
        },
    });

    $("#sortByID").click(updateSort);
    $("#sortByName").click(updateSort);
    $("#sortAsc").click(updateSort);
    $("#sortDesc").click(updateSort);
});
