$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/api/manifest",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (result) {
            // .hide() is not sufficient to override 'display: flex !important' in class 'd-flex'
            $("#loadingSpinner").css("display", "none", "important");
            $("#dataContainer").text(JSON.stringify(result, null, 2));
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
