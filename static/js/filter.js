$(document).ready(function () {
    $("#filtersToggleButton").click(function (event) {
        event.preventDefault();
        $("#filtersMenu").toggleClass("hide-by-default");
    });
});
