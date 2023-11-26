from Crypto.Util.number import bytes_to_long, long_to_bytes
from randcrack import RandCrack
from tqdm import tqdm
import random
import requests

def xor(a, b):
    return b''.join([bytes([_a ^ _b]) for _a, _b in zip(a, b)])

# cookies = dict(session="dcc17656-ec4a-4084-985c-fbad887ff8b7.IYl1FJcdbJgPeCrs8ebdPfuoZgQ")

URL = "http://ctf.tcp1p.com:54734/"

with open("test.txt", "wb") as FILE:
    FILE.write(b"\x00"*4)

def send_file():
    files = {'file': open('test.txt', 'rb')}
    r = requests.post(URL, files=files)
    return r.content

def get_flag():
    r = requests.get(URL + "flago")
    return r.content

rc = RandCrack()

for _ in tqdm(range(624)):
    r = bytes_to_long(send_file())
    rc.submit(r)

c_flag = get_flag()

with open("flag-enc.jpg", "wb") as FILE:
    FILE.write(c_flag)

key = long_to_bytes(rc.predict_getrandbits(len(c_flag)*8))

with open("key", "wb") as FILE:
    FILE.write(key)

assert len(key) == len(c_flag)

flag = xor(c_flag, key)

with open("flag.jpg", "wb") as FILE:
    FILE.write(flag)