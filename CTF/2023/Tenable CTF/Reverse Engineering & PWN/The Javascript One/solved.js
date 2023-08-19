var flag = "Zm1jZH92N2tkcFVhbXs6fHNjI2NgaA==";

function encryptFlag(plain) {
  var res = "";
  for (var i = 0; i < plain.length; i++) {
    var b = plain.charCodeAt(i) ^ i;
    res += String.fromCharCode(b);
  }
  return btoa(res);
}

function decryptFlag(cipher) {
  var res = "";
  var plain = atob(cipher);
  for (var i = 0; i < plain.length; i++) {
    var b = plain.charCodeAt(i) ^ i;
    res += String.fromCharCode(b);
  }
  return res;
}

console.log(decryptFlag(flag));