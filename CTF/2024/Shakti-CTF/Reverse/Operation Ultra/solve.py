import base64


def xoring(flag, key):
    flag_len = len(flag)
    unk_str_len = len(key)

    res = bytearray(flag, "utf-8")

    for i in range(flag_len):
        res[i] = res[i] ^ ord(key[i % unk_str_len])

    return res.decode("utf-8")


def func_2(flag):
    flag_len = len(flag)
    res = [""] * flag_len

    j = 0

    for i in range(0, flag_len, 4):
        res[j] = flag[i]
        res[j + 1] = flag[i + 1]
        j += 2

    for i in range(2, flag_len, 4):
        res[j] = flag[i]
        res[j + 1] = flag[i + 1]
        j += 2

    return "".join(res)


def rev_func_2(flag):
    for _ in range(3):
        flag = func_2(flag)
    return flag


key = "U2hhZG93MjAyNA=="
key = base64.b64decode(key.encode("ascii")).decode("ascii")

c = [
    32,
    0,
    27,
    30,
    84,
    79,
    86,
    22,
    97,
    100,
    63,
    95,
    60,
    34,
    1,
    71,
    0,
    15,
    81,
    68,
    6,
    4,
    91,
    40,
    87,
    0,
    9,
    59,
    81,
    83,
    102,
    21,
]
c = "".join([chr(x) for x in c])

flag = rev_func_2(c)
flag = xoring(flag, key)
print(flag)
