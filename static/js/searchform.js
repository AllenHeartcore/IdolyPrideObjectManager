function keywordFilter(alias) {
    let query = $("#searchInput").val();
    if (query !== "" && query.slice(-1) !== " ") {
        // the user has typed something, but we need a trailing space
        // to recognize our alias as a separate keyword
        query += " ";
    }
    $("#searchInput").val(`${query}${alias} `); // so the user can directly continue
    $("#searchInput").focus();
}

function buildButtonList(containerID, eltList, columnClass) {
    for (let name of eltList) {
        let column = $("<div>").addClass(columnClass);
        let button = $("<button>")
            .attr("type", "button") // otherwise submits the form
            .addClass("btn btn-outline-primary btn-sm w-100 mb-2")
            .attr("onclick", `keywordFilter('${name}')`)
            .text(name);
        column.append(button);
        $(containerID).append(column);
    }
}

function buildFiltersMenu() {
    buildButtonList("#filtersSongContainer", SONG_LIST, "col-md-4");

    for (let name in CHARACTER_ALIAS) {
        let alias = CHARACTER_ALIAS[name];
        let column = $("<div>").addClass("col-md-1");
        let img = $("<img>")
            .attr("id", "filtersCharacterFigure")
            .attr("src", `/static/img/figure/${alias}.png`)
            .attr("alt", name)
            .attr("onclick", `keywordFilter('${name}')`);
        column.append(img);
        $("#filtersCharacterContainer").append(column);
    }
}

$(document).ready(function () {
    buildFiltersMenu();

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

    $("#searchInput").focus(function () {
        if ($("#filtersMenu").is(":visible")) {
            return;
            // otherwise, clicking on filters in the menu triggers a focus on the search bar,
            // which then immediately hides the menu and slowly shows it again
        }
        $("#filtersMenu").removeClass("slide-out").show().addClass("slide-in");
        $("#filtersMenu").one("animationend", function () {
            $(this).removeClass("slide-in");
        });
    });

    // the menu should only hide when the user is
    // NEITHER clicking on the menu NOR focusing on the search input
    $(document).mouseup(function (e) {
        if (!$("#filtersMenu").is(":visible")) {
            return;
            // otherwise, the animation works just fine when the page first loads,
            // but clicking randomly on the page will add style="display: none;"
            // to the menu, which interferes with the menu and makes it glitch out
            // at animation complete when the user tries to show it again
        }
        var container = $("#filtersMenu, #searchInput");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            $("#filtersMenu").removeClass("slide-in").addClass("slide-out");
            $("#filtersMenu").one("animationend", function () {
                $(this).hide().removeClass("slide-out");
            });
        }
    });
});
