const CHARACTER_ALIAS = {
    "Hanami Saki": "hski",
    "Tsukimura Temari": "ttmr",
    "Fujita Kotone": "fktn",
    "Arimura Mao": "amao",
    "Katsuragi Lilja": "kllj",
    "Kuramoto China": "kcna",
    "Shiun Sumika": "ssmk",
    "Shinosawa Hiro": "shro",
    "Himesaki Rinami": "hrnm",
    "Hanami Ume": "hume",
    "Hataya Misuzu": "hmsz",
    "Juo Sena": "jsna",
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
