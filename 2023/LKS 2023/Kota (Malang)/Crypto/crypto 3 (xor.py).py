#/usr/bin/python3
from base64 import b64encode

def encrypt(plain):
    key = "n0k3y"
    cipher = ""
    for c, i in enumerate(plain):
        cipher += chr(ord(i) ^ ord(key[c % 5]))

    print(b64encode(cipher.encode()))

if __name__ == "__main__":
    plain = input()
    encrypt(plain)