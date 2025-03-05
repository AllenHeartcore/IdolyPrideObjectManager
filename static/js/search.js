function populateSearchResults(data) {}

function reportSearchError() {}

$(document).ready(function () {
    console.log("Search page ready!");
    console.log(query);
    $.ajax({
        type: "GET",
        url: `/api/search/${query}`,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            console.log(result);
            populateSearchResults(result);
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
