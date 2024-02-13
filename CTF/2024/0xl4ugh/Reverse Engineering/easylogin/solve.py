from base64 import b64decode


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


token = b"141414_161616"

CT = b"pDG/SbSehGM2l16sRzFmxRDZNCti2PNXzY9Z"
CT = b64decode(CT)

password = rc4(CT, token)
print(password)
