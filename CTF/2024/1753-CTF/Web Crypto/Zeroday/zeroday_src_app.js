const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const initSQL = require('sql.js');
const smoltok = require('smoltok');
const crypto = require('crypto');

const app = express();
app.set('view engine', 'ejs');

const port = 1337;

const secret = crypto.randomBytes(64).toString("hex");

let db;

initSQL().then(async sql => {
    db = new sql.Database();

    db.exec("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)");
    db.exec("CREATE TABLE bugs (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))");
    db.exec("INSERT INTO users (id, username, password) VALUES (1, 'adam', 'pwd')");
    db.exec("INSERT INTO users (id, username, password) VALUES (2, 'admin', '" + crypto.randomBytes(40).toString("hex") + "')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (1, 1, 'Donut dispenser is getting stuck twice a day')");
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (2, 1, 'Coffee machine brews tea')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (3, 2, '" + (process.env.flag || "1753c{fake_flag}") + "')")
});

app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static("public"));

app.get('/login', (req, res) => {
    res.render("login");
})

app.post('/login', (req, res) => {
    const stmt = db.prepare("SELECT * FROM users WHERE username=:username AND password=:password");
    stmt.bind({ ':username': req.body["username"], ':password': req.body["password"] });

    if (!stmt.step()) {
        res.render("login", { error: "Incorrect login" });
    }
    else {
        const token = smoltok.encode({ "username": req.body["username"] }, secret);
        res.cookie("token", token);
        res.redirect("/");
    }

    stmt.free();
})

app.use((req, res, next) => {
    try {
        const token = req.cookies.token;
        req.user = smoltok.decode(token, secret);
        next();
    }
    catch (err) {
        res.redirect("/login")
    }

})

app.get('/', (req, res) => {
    const results = db.exec("SELECT b.title FROM bugs b JOIN users u ON b.user_id = u.id WHERE u.username like '" + req.user.username + "'")
    res.render("bugs", { results: results && results.length > 0 ? results[0].values : [], user: req.user })
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
})