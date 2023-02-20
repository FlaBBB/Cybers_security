from base64 import b64encode, b64decode

def encrypt(plain):
    key = "n0k3y"
    cipher = ""
    for c, i in enumerate(plain):
        cipher += chr(ord(i) ^ ord(key[c % 5]))

    print(b64encode(cipher.encode()))

# if __name__ == "__main__":
#     plain = input()
#     encrypt(plain)

def decrypt(cipher):
    cipher = b64decode(cipher.encode()).decode()
    key = "n0k3y"
    uncipher = ""
    for c, i in enumerate(cipher):
        uncipher+=chr(ord(i)^ord(key[c%5]))

    return uncipher



print(decrypt("Ins4AUlcAyZSFQ9eDEgAIUU0V0oNQhJDDTFdWE4="))