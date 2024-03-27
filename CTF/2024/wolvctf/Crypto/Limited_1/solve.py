import random

cipher = [
    189,
    24,
    103,
    164,
    36,
    233,
    227,
    172,
    244,
    213,
    61,
    62,
    84,
    124,
    242,
    100,
    22,
    94,
    108,
    230,
    24,
    190,
    23,
    228,
    24,
]

for seed in range(256):
    res = b""
    for i in range(len(cipher)):
        random.seed(i + seed)
        res += bytes([cipher[i] ^ random.getrandbits(8)])
    if res.decode("latin-1").isprintable() and res.decode("latin-1").isascii():
        print(res)
