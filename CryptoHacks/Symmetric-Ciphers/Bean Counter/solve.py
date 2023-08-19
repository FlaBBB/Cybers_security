import requests

def get_encrypted():
    r = requests.get("https://aes.cryptohack.org/bean_counter/encrypt/")
    return r.json()["encrypted"]

png_header_16byte = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D\x49\x48\x44\x52"

cipher = bytes.fromhex(get_encrypted())

keystream = b""
for i in range(16):
    keystream += bytes([png_header_16byte[i] ^ cipher[i]])

res = b""
for i in range(len(cipher)):
    res += bytes([cipher[i] ^ keystream[i % 16]])

with open("flag.png", "wb") as f:
    f.write(res)