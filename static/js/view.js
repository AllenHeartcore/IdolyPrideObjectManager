function displayMedia() {
    getMediaBlobURL(type, info.id).then(({ url, mimetype }) => {
        $("#loadingSpinnerMedia").hide();
        $("#viewMediaContent").show();
        let container = $("#viewMediaContent");

        if (mimetype.startsWith("image/")) {
            container.append(
                $("<img>").attr("src", url).attr("alt", info.name)
            );
        } else if (mimetype.startsWith("audio/")) {
            container.append(
                $("<audio>")
                    .attr({ src: url, controls: true })
                    .attr("alt", info.name)
            );
        } else if (mimetype.startsWith("video/")) {
            container.append(
                $("<video>")
                    .attr({ src: url, controls: true })
                    .attr("alt", info.name)
            );
        } else if (mimetype === "application/zip") {
            fetch(url)
                .then((response) => response.blob())
                .then((blob) => JSZip.loadAsync(blob))
                .then((zip) => {
                    Object.keys(zip.files).forEach((filename) => {
                        let row = $("<div>").addClass("row align-center gy-2");
                        let col1 = $("<div>").addClass("col-2 align-left fs-5");
                        let col2 = $("<div>").addClass("col-10");

                        let alias = filename.split(".")[0].split("_").pop();
                        col1.text(alias);

                        zip.files[filename].async("blob").then((fileBlob) => {
                            const fileUrl = URL.createObjectURL(fileBlob);
                            col2.append(
                                $("<audio>")
                                    .attr({ src: fileUrl, controls: true })
                                    .attr("alt", filename)
                            );
                        });

                        row.append(col1).append(col2);
                        container.append(row);
                    });
                })
                .catch((...args) => {
                    dumpErrorToConsole(...args);
                    handleUnsupportedMedia(url);
                });
        } else {
            handleUnsupportedMedia(url);
            return;
        }

        $("#downloadConvertedMedia")
            .text("Download Converted " + mimetype.split("/")[1].toUpperCase())
            .attr("href", url)
            .attr("download", info.name.replace(/\.[^/.]+$/, ""))
            .removeClass("disabled");
    });
}

function handleUnsupportedMedia(url) {
    $("#viewMediaContent").append(
        $("<div>").text("Preview not available for this type of media.")
    );
    if (type === "AssetBundle") {
        $("#downloadConvertedMedia")
            .text("Deobfuscated AssetBundle")
            .attr("href", url)
            .attr("download", info.name.replace(/\.[^/.]+$/, "") + ".unity3d")
            .removeClass("disabled");
    } else {
        $("#downloadConvertedMedia")
            .text("Conversion Unavailable")
            .removeClass("btn-primary")
            .addClass("btn-secondary");
    }
}

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

    displayMedia();
    displayCaption();
});
