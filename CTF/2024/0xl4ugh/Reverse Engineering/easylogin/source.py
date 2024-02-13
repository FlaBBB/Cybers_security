from base64 import b64encode

TARGET = b"pDG/SbSehGM2l16sRzFmxRDZNCti2PNXzY9Z"

_b64encode = b64encode


def b64encode(data):
    return _b64encode(data).replace(b"=", b"")


def key_schedule(token: bytes):
    sbox = bytearray(range(256))
    k = 0
    for i in range(256):
        k = (k + sbox[i] + token[i % len(token)]) % 256
        sbox[i], sbox[k] = sbox[k], sbox[i]
    return sbox


def rc4(password: bytes, token: bytes):
    sbox = key_schedule(token)
    res = bytearray(password)
    j = 0
    k = 0
    for i in range(len(res)):
        j = (j + 1) % 256
        k = (k + sbox[j]) % 256
        sbox[j], sbox[k] = sbox[k], sbox[j]
        res[i] ^= sbox[(sbox[j] + sbox[k]) % 256]
    return res


def main():
    username = input("Enter username: ").encode()
    password = input("Enter password: ").encode()
    token = input("Enter token: ").encode()
    password = rc4(password, token)
    if b64encode(password) == TARGET:
        print(f"Login successful!\nFlag is 0xl4ugh{{{password}}}")
    else:
        print("Login failed. Incorrect username or password.")
