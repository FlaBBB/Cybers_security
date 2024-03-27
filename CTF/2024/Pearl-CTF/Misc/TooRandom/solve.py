import requests
from randcrack import RandCrack

HOST = "https://toorandom-e1aacd4d0b6dbf62.ctf.pearlctf.in"


def get_number():
    url = f"{HOST}/dashboard"
    r = requests.get(url)
    assert r.status_code == 200
    # print(r.text)
    number = r.text.split("Number : ")[1].split("<")[0]
    return int(number)


rc = RandCrack()

for _ in range(624):
    rc.submit(get_number())

for i in range(10000 - 624):
    flag_no = rc.predict_getrandbits(32)