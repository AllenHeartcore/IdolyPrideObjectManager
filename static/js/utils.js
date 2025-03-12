const CHARACTER_ALIAS = {
    "hski": "Hanami Saki",
    "ttmr": "Tsukimura Temari",
    "fktn": "Fujita Kotone",
    "amao": "Arimura Mao",
    "kllj": "Katsuragi Lilja",
    "kcna": "Kuramoto China",
    "ssmk": "Shiun Sumika",
    "shro": "Shinosawa Hiro",
    "hrnm": "Himesaki Rinami",
    "hume": "Hanami Ume",
    "hmsz": "Hataya Misuzu",
    "jsna": "Juo Sena",
};

const SONG_ALIAS = {
    "all-001": "初",
    "all-002": "Campus mode!!",
    "all-003": "キミとセミブルー",
    "all-004": "冠菊",
    "all-005": "仮装狂騒曲",
    "all-006": "White Night! White Wish!",
    "all-007": "ハッピーミルフィーユ",
    "all-008": "古今東西ちょちょいのちょい",
    "all-009": "雪解けに",
    "char-001": "(1st Single)",
    "char-002": "(2nd Single)",
    "char-003": "(2024-25 Birthday Song)",
};

function dumpErrorToConsole(...args) {
    var name_of_parent_function = arguments.callee.caller.name;
    console.log("Error in " + name_of_parent_function);
    args.forEach((arg) => {
        console.log(arg);
    });
}
