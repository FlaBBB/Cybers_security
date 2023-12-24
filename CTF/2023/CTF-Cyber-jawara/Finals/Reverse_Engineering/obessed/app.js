const express = require('express');
const cors = require('cors-express-middleware');
const md5 = require("crypto-js/md5");
const sha1 = require("crypto-js/sha1");
const sha224 = require("crypto-js/sha224");
const sha256 = require("crypto-js/sha256");
const sha384 = require("crypto-js/sha384");
const sha512 = require("crypto-js/sha512");
const ripemd160 = require("crypto-js/ripemd160");

const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.json({ service: "obsessed", version: "1.33.7" });
});

app.post('/hash/md5', (req, res) => {
    const { text } = req.body;
    const data = md5(text).toString();
    res.json({ data });
});

app.post('/hash/sha1', (req, res) => {
    const { text } = req.body;
    const data = sha1(text).toString();
    res.json({ data });
});

app.post('/hash/sha224', (req, res) => {
    const { text } = req.body;
    const data = sha224(text).toString();
    res.json({ data });
});

app.post('/hash/sha256', (req, res) => {
    const { text } = req.body;
    const data = sha256(text).toString();
    res.json({ data });
});

app.post('/hash/sha384', (req, res) => {
    const { text } = req.body;
    const data = sha384(text).toString();
    res.json({ data });
});

app.post('/hash/sha512', (req, res) => {
    const { text } = req.body;
    const data = sha512(text).toString();
    res.json({ data });
});


app.post('/hash/ripemd160', (req, res) => {
    const { text } = req.body;
    const data = ripemd160(text).toString();
    res.json({ data });
});

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});



