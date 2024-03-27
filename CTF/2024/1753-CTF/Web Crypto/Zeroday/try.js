var input = {
    "user": "admin",
    "password": "pwd"
}

const data = new URLSearchParams(input).toString();
console.log(data);

const forged_token = "dXNlcj1hZG1pbiZwYXNzd29yZD1wd2SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEuCZhbm90aGVyPWJsYWJsYWJsYQ.MC_fIbS1ITH-0Kx6O178Icm3Cxg";
var forged_data = decode(forged_token, secret);
console.log(forged_data);