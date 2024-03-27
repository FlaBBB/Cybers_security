def xor(msg, key):
    st = ""
    for i in range(len(msg)):
        st += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return st


with open("msg", "r", encoding="utf-8") as f:
    msg = "".join(f.readlines()).rstrip("\n")

with open("key", "r", encoding="utf-8") as k:
    key = "".join(k.readlines()).rstrip("\n")

assert key.isalnum()

with open("encrypted", "w") as fo:
    fo.write(xor(msg, key))
