const ACCENT_COLORS = {
    "hski": "#942522",
    "ttmr": "#2A2175",
    "fktn": "#FBE6AA",
    "hrnm": "#FFE2D9",
    "ssmk": "#D0F3B9",
    "shro": "#BAF0E8",
    "kllj": "#EBEBFF",
    "kcna": "#DE6429",
    "amao": "#41295E",
    "hume": "#E55039",
    "jsna": "#C6904A",
};

function hex2rgb(hex) {
    return [
        parseInt(hex.slice(1, 3), 16),
        parseInt(hex.slice(3, 5), 16),
        parseInt(hex.slice(5, 7), 16),
    ];
}

function rgb2hsl(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;
    let max = Math.max(r, g, b);
    let min = Math.min(r, g, b);
    let h,
        s,
        l = (max + min) / 2;
    if (max == min) {
        h = s = 0;
    } else {
        let d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }
    return [h, s, l];
}

function setRandomAccentColor() {
    let keys = Object.keys(ACCENT_COLORS);
    let key = keys[Math.floor(Math.random() * keys.length)];
    let accent = ACCENT_COLORS[key];
    let hsl = rgb2hsl(...hex2rgb(accent));

    console.log(accent, hsl);
    $("#navbarSticker").attr("src", `/static/stickers/${key}.png`);
    $(".navbar").css(
        "background-color",
        `hsl(${hsl[0] * 360}, ${hsl[1] * 100}%, 90%)`
    );
    $("#navbarText").css("color", `hsl(${hsl[0] * 360}, 50%, 50%)`);
}

$(document).ready(function () {
    setRandomAccentColor();
    $("#navbarSticker").click(setRandomAccentColor);
});
