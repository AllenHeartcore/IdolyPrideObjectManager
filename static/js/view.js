function getCaption() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: `/api/${type.toLowerCase()}/${info.id}/caption`,
            dataType: "text",
            contentType: "charset=utf-8",
            success: function (caption) {
                resolve(caption);
            },
            error: function (...args) {
                dumpErrorToConsole(...args);
                reject("[An error occurred while generating caption.]");
            },
        });
    });
}

function displayCaption() {
    getCaption().then((caption) => {
        $("#loadingSpinnerCaption").hide();
        $("#viewCaptionText").show();
        $("#viewCaptionText").text(caption);
    });
}

$(document).ready(function () {
    setAccentColorByString(info.name);
    displayCaption();
});
