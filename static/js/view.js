$(document).ready(function () {
    for (let keyword of info.keywords) {
        let alias = CHARACTER_ALIAS[keyword];
        if (alias) {
            setAccentColorByString(alias);
            // there's still a tiny delay
        }
    }
});
