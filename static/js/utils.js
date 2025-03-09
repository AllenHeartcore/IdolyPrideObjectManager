function dumpErrorToConsole(...args) {
    var name_of_parent_function = arguments.callee.caller.name;
    console.log("Error in " + name_of_parent_function);
    args.forEach((arg) => {
        console.log(arg);
    });
}

// Search event listener
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

// Override Enter key
function enterKeyOverriderFactory(form_id) {
    return function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $(form_id).submit();
        }
    };
}

function getMediaBlob(type, id) {
    $.ajax({
        type: "GET",
        url: `/api/${type.toLowerCase()}/${id}/bytestream`,
        xhrFields: { responseType: "arraybuffer" },
    })
        .then(function (data, status, request) {
            const mimetype = request.getResponseHeader("Content-Type");
            return new Blob([data], { type: mimetype });
        })
        .catch(function (...args) {
            dumpErrorToConsole(...args);
            return new Blob(["An error occurred while fetching media."], {
                type: "text/plain",
            });
        });
}
