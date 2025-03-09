$(document).ready(function () {
    setRandomAccentColor();

    // Search event listener
    $("#navbarSearchForm").submit(function (event) {
        event.preventDefault();
        let query = $("#navbarSearchInput").val();
        if (!query.trim()) {
            $("#navbarSearchInput").val("");
            $("#navbarSearchInput").focus();
            return;
        }
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
    });

    // Override Enter key
    $("#navbarSearchInput").keydown(function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#navbarSearchForm").submit();
        }
    });
});
