def b(inp):
    res = ""
    i = 0
    while i < len(inp):
        c = inp[i]
        res += chr(ord(c) ^ 538501427 ^ 0x20182D44)
        i += 1
    return res


# ct = "찾찙찔찘찅찅찒찔찃챗찇찖찄찄찀찘찅찓챖"
# print(b(ct).encode())

from base64 import b64decode, b64encode


def password_encryptor(password):
    res = [x for x in password.encode()]
    for i in range(1, len(res) + 1):
        for j in range(len(res)):
            res[j] = (res[j] + (i - 12) * j + 6) & 0xFF
    return b64encode(bytes(res)).encode("utf-16be")


def password_decryptor(password):
    res = password.encode("utf-16be")
    if b"\xff\xfe" in res:
        res = res[2:]
    res = b64decode(res)
    res = [x for x in res]
    for i in range(1, len(res) + 1):
        for j in range(len(res)):
            res[j] = (res[j] - (i - 12) * j - 6) & 0xFF
    return bytes(res)


ct = "렒蘐鱇騢鼡謴꼾︻ꁏ꤅뤃ꔍ먅ꈽ"
print(password_decryptor(b(ct)))
