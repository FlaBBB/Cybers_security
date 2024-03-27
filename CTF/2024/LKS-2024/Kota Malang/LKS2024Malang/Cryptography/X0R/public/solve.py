import string

key_dict = (string.ascii_letters + string.digits).encode()

enc = open("encrypted", "rb").read()
known_text = "LKS2024Malang{"
limit_key_length = len(known_text)


def xor(x, key):
    st = bytearray()
    for i in range(len(x)):
        st.append(x[i] ^ key[i % len(key)])
    return bytes(st)


def check_key(enc: bytes, pt: str, off: int, n: int):
    _pt = pt.ljust(n, "\x00").encode("latin-1")[:n]
    for i, e in enumerate(enc[off : off + n]):
        if i < len(pt) and bytes([e ^ _pt[i]]) not in key_dict:
            return False
    return True


def check_printable(x: bytes):
    return all(chr(e) in string.printable for e in x)


possible_known_text = dict()
for n in range(1, limit_key_length + 1):
    for i in range(len(enc) - n):
        if check_key(enc, known_text, i, n) and possible_known_text.get(i, 0) < n:
            possible_known_text[i] = n

possible_key = []
for off, n in possible_known_text.items():
    key = bytearray(n)
    for i in range(n):
        key[i] = enc[off + i] ^ ord(known_text[i])
    key = bytes(key).decode()
    for _ in range(i % n):
        key = key[-1] + key[:-1]
    possible_key.append(key)

for key in possible_key:
    for n in range(1, len(key)):
        res = xor(enc, key[:n].encode())
        if check_printable(res):
            print(res)
