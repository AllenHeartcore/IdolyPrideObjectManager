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

const SONG_LIST = [
    "初",
    "Campus mode!!",
    "キミとセミブルー",
    "冠菊",
    "仮装狂騒曲",
    "White Night! White Wish!",
    "ハッピーミルフィーユ",
    "古今東西ちょちょいのちょい",
    "雪解けに",
    "1st Single",
    "2nd Single",
    "Birthday Single",
];

function dumpErrorToConsole(...args) {
    var name_of_parent_function = arguments.callee.caller.name;
    console.log("Error in " + name_of_parent_function);
    args.forEach((arg) => {
        console.log(arg);
    });
}
