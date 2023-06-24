document.getElementById("submit").addEventListener("click", function() {
    fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "text/plain"
        },
        body: JSON.stringify({
            "username": document.getElementById("username").value,
            "secret": document.getElementById("secret").value == undefined ? "" : document.getElementById("secret").value,
            "role": document.getElementById("secret").value == undefined ? "User" : "Admin"
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("response").innerHTML = data.message;
            if(data.secret) {
                document.getElementById("response").innerHTML += "<br>" + data.secret;
            }
        }
    })
});