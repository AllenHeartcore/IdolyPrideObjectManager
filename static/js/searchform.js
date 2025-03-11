$(document).ready(function () {
    $("#searchForm").submit(function (event) {
        event.preventDefault();
        let query = $("#searchInput").val();
        if (!query.trim()) {
            $("#searchInput").val("");
            $("#searchInput").focus();
            return;
        }
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
    });

    $("#searchInput").keydown(function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#searchForm").submit();
        }
    });

    $("#filtersToggleButton").click(function (event) {
        event.preventDefault();
        $("#filtersMenu").toggleClass("hide-by-default");
    });
});
