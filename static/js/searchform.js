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

function buildButtonList(containerID, aliasMap, columnClass) {
    for (let alias in aliasMap) {
        let name = aliasMap[alias];
        let column = $("<div>").addClass(columnClass);
        let button = $("<button>")
            .attr("type", "button") // otherwise submits the form
            .addClass("btn btn-outline-primary btn-sm w-100 mb-2")
            .attr("onclick", `keywordFilter('${alias}')`)
            .text(name);
        column.append(button);
        $(containerID).append(column);
    }
}

function buildFiltersMenu() {
    buildButtonList("#filtersMediaContainer", MEDIA_ALIAS, "col-md-3");
    buildButtonList("#filtersSubtypeContainer", SUBTYPE_ALIAS, "col-md-3");
    buildButtonList("#filtersRarityContainer", RARITY_ALIAS, "col-md-4");
    buildButtonList("#filtersSongContainer", SONG_ALIAS, "col-md-4");

    for (let alias in CHARACTER_ALIAS) {
        let name = CHARACTER_ALIAS[alias];
        let column = $("<div>").addClass("col-md-1");
        let img = $("<img>")
            .attr("src", `../static/img/figure/${alias}.png`) // Jinja's url_for doesn't work here
            .attr("id", "filtersCharacterFigure")
            .attr("alt", name)
            .attr("onclick", `keywordFilter('${alias}')`);
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

    $("#filtersToggleButton").click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        // otherwise, this event will bubble up to the document
        // and immediately hide the menu again, as defined below
        $("#filtersMenu").toggleClass("hide-by-default");
    });

    $(document).click(function (event) {
        if (!$(event.target).closest("#filtersMenu").length) {
            $("#filtersMenu").addClass("hide-by-default");
        }
    });
});
