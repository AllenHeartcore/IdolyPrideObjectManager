function searchEventListenerFactory(input_field_id) {
    return function (event) {
        event.preventDefault();
        let query = $(input_field_id).val();
        if (!query.trim()) {
            $(input_field_id).val("");
            $(input_field_id).focus();
            return;
        }
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
    };
}

function enterKeyOverriderFactory(form_id) {
    return function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $(form_id).submit();
        }
    };
}

$(document).ready(function () {
    $("#filtersToggleButton").click(function (event) {
        event.preventDefault();
        $("#filtersMenu").toggleClass("hide-by-default");
    });
});
