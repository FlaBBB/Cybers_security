import json
import requests
import string
from time import sleep

DICT = string.ascii_letters + string.digits + string.punctuation + " "

def encrypt(plaintext: bytes) -> bytes:
    plaintext = plaintext.hex()
    while True:
        try:
            req = requests.get("http://aes.cryptohack.org/ecb_oracle/encrypt/" + plaintext)
            break
        except requests.exceptions.ConnectionError:
            sleep(1)
            continue
    return bytes.fromhex(json.loads(req.content.strip().decode())['ciphertext'])

def attack(encrypt_oracle, unused_byte=0):
    """
    Recovers a secret which is appended to a plaintext and encrypted using ECB.
    :param encrypt_oracle: the encryption oracle
    :param unused_byte: a byte that's never used in the secret
    :return: the secret
    """
    paddings = [bytes([unused_byte] * i) for i in range(16)]
    secret = bytearray(b"crypto{")
    while True:
        padding = paddings[15 - (len(secret) % 16)]
        p = bytearray(padding + secret + b"0" + padding)
        byte_index = len(padding) + len(secret)
        end1 = len(padding) + len(secret) + 1
        end2 = end1 + len(padding) + len(secret) + 1
        for i in DICT:
            i = ord(i)
            p[byte_index] = i
            c = encrypt_oracle(p)
            if c[end1 - 16:end1] == c[end2 - 16:end2]:
                secret.append(i)
                break
        else:
            secret.pop()
            break
        print(bytes(secret))

    return bytes(secret)

print(attack(encrypt))