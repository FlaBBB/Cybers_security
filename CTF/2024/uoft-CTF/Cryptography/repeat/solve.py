import string

ct = "982a9290d6d4bf88957586bbdcda8681de33c796c691bb9fde1a83d582c886988375838aead0e8c7dc2bc3d7cd97a4"
ct = bytes.fromhex(ct)


def check_xor_key(ct, char, off, format_flag, repeat=8):
    for i in range(off, len(ct), repeat):
        res = chr(ct[i] ^ char)
        if res not in string.printable:
            return False
        if i < len(format_flag) and res != format_flag[i]:
            return False
    return True


def xor(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])


key = b""
format_flag = "uoftctf{"

for i in range(8):
    for c in range(0x100):
        if check_xor_key(ct, c, i, format_flag):
            key += bytes([c])

print(xor(ct, key))
