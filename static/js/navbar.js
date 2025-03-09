$(document).ready(function () {
    setRandomAccentColor();

    $("#navbarSearchForm").submit(
        searchEventListenerFactory("#navbarSearchInput")
    );

    $("#navbarSearchInput").keydown(
        enterKeyOverriderFactory("#navbarSearchForm")
    );
});
