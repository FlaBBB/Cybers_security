from itertools import product

from tqdm import tqdm

ct = "a81c0750d48f0750"


def worble(s):
    s1 = 5
    s2 = 31

    for n in range(len(s)):
        s1 = (s1 + ord(s[n]) + 7) % 65521
        s2 = (s1 * s2) % 65521
    return (s2 << 16) | s1


def shmorble(s):
    r = ""
    for i in range(len(s)):
        r += s[i - len(s)]

    return r


def blorble(a, b):
    return format(a, "x") + format(b, "x")


for f in tqdm(product("bdrw013", repeat=9), total=7**9):
    flag = "uoftctf{" + "".join(f) + "}"
    a = worble(flag)
    b = worble(flag[::-1])
    res = shmorble(blorble(a, b))
    if res == ct:
        print(flag)
        break
