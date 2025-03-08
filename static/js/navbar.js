$(document).ready(function () {
    setRandomAccentColor();
    $("#navbarSticker").click(setRandomAccentColor);

    // Search event listener
    $("#searchForm").submit(function (event) {
        event.preventDefault();
        let query = $("#searchInput").val();
        if (!query.trim()) {
            $("#searchInput").val("");
            $("#searchInput").focus();
            return;
        }
        window.location.href = `/search/${query}`;
    });

    // Override Enter key
    $("#searchInput").keydown(function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#searchForm").submit();
        }
    });
});
