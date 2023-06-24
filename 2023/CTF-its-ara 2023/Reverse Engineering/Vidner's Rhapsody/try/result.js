function mystenc(berserk, guts) {
    var s = [], j = 0, x, res = '';
    for (var i = 0; i < 256; i++) {
        s[i] = i;
    }
    for (i = 0; i < 256; i++) {
        j = (j + s[i] + berserk.charCodeAt(i % berserk.length)) % 256;
        x = s[i];
        s[i] = s[j];
        s[j] = x;
    }
    i = 0;
    j = 0;
    for (var y = 0; y < guts.length; y++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        x = s[i];
        s[i] = s[j];
        s[j] = x;
        res += String.fromCharCode(guts[y] ^ s[(s[i] + s[j]) % 256]);
    }
    console.log(res);
}
var berserk = 'achenk';
var strenk = [
    244,
    56,
    117,
    247,
    61,
    16,
    3,
    64,
    107,
    57,
    131,
    13,
    137,
    113,
    214,
    238,
    178,
    199,
    4,
    115,
    235,
    139,
    201,
    22,
    164,
    132,
    175
];
mystenc(berserk, strenk);