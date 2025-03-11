$(document).ready(function () {
    setRandomAccentColor();

    $("#navbarSearchForm").css("width", "25%");
    $("#searchButton").css("font-size", "1rem");

    $("#navbarSearchForm").submit(searchEventListenerFactory("#searchInput"));

    $("#searchInput").keydown(enterKeyOverriderFactory("#navbarSearchForm"));
});
