# /usr/bin/python3


from base64 import b64decode
from base64 import b64encode


def encrypt(plain):
    key = "n0k3y"
    cipher = ""
    a = 1
    for c, i in enumerate(plain):
        cipher += chr(ord(i) ^ ord(key[c % 5]))

    print(b64encode(cipher.encode()))

# if __name__ == "__main__":
#     plain = input()
#     encrypt(plain)


encrypt("LKS30SMK{y0u_d3crypt_m3}")
# cipher=Ins4AEk9fSBIAF5FNFdKDUISQw0xXVhO


# Solving

def decrypt(cipher):
    key = "n0k3y"
    cipher = b64decode(cipher).decode()
    plain = ""
    for c, i in enumerate(cipher):
        plain += chr(ord(i) ^ ord(key[c % 5]))
    print(plain)


decrypt("Ins4AEk9fSBIAF5FNFdKDUISQw0xXVhO")
