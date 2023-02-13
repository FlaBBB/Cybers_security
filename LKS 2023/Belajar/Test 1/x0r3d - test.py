# /usr/bin/python3


from base64 import b64decode
from base64 import b64encode


def encrypt(plain):
    key = "n0k3y"
    cipher = ""
    a = 1
    for c, i in enumerate(plain):
        # print("1. "+str(a))
        # print("2. "+str(c))
        # print("3. "+str(ord(i)))
        # print(ord(i) ^ ord(key[c % 5]))
        cipher += chr(ord(i) ^ ord(key[c % 5]))
        # print(cipher)
        # a+=1

    # print(cipher)
    # print(b64encode(cipher.encode("ascii")).decode("ascii"))
    print(b64encode(cipher.encode("ascii")))
    print(cipher.encode())

# if __name__ == "__main__":
#     plain = input()
#     encrypt(plain)







encrypt("aku")
# cipher=Ins4AEk9fSBIAF5FNFdKDUISQw0xXVhO

cipher = ""
# Solving


def decrypt(cipher):
    key = "n0k3y"
    cipher = b64decode(cipher[2:-1]).decode()
    i = 0
    plain = ""
    for a in cipher:
        # print(ord(a))
        plain += chr(ord(a) ^ ord(key[i % 5]))
        i += 1
    print(plain)


decrypt("b'J14YBzgrW1JVKix5KnVMKH4tVzIqZSJgKBkAE2svBn8='")
