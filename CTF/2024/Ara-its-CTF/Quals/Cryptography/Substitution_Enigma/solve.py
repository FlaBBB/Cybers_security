from itertools import product

cycle = 5
block_size = 8
s1 = {
    0: 15,
    1: 2,
    2: 14,
    3: 0,
    4: 1,
    5: 3,
    6: 10,
    7: 6,
    8: 4,
    9: 11,
    10: 9,
    11: 7,
    12: 13,
    13: 12,
    14: 8,
    15: 5,
}
s2 = {
    0: 12,
    1: 8,
    2: 13,
    3: 6,
    4: 9,
    5: 1,
    6: 11,
    7: 14,
    8: 5,
    9: 10,
    10: 3,
    11: 4,
    12: 0,
    13: 15,
    14: 7,
    15: 2,
}
inv_s1 = {v: k for k, v in s1.items()}
inv_s2 = {v: k for k, v in s2.items()}

to_bin = lambda x, n=block_size: format(x, "b").zfill(n)
to_int = lambda x: int(x, 2)
to_chr = lambda x: "".join([chr(i) for i in x])
to_ord = lambda x: [ord(i) for i in x]
bin_join = lambda x, n=int(block_size / 2): (str(x[0]).zfill(n) + str(x[1]).zfill(n))
bin_split = lambda x: (x[0 : int(block_size / 2)], x[int(block_size / 2) :])
str_split = lambda x: [x[i : i + block_size] for i in range(0, len(x), block_size)]
xor = lambda x, y: x ^ y


def inv_s(a, b):
    return inv_s1[a], inv_s2[b]


def inv_p(a):
    return a[5] + a[3] + a[1] + a[2] + a[7] + a[0] + a[4] + a[6]


def rnd_keys(k):
    return [
        k[i : i + int(block_size)] + k[0 : (i + block_size) - len(k)]
        for i in range(cycle)
    ]


def xkey(state, k):
    return [xor(state[i], k[i]) for i in range(len(state))]


def inv_en(c):
    decrypted = []
    for i in c:
        pe = to_bin(ord(i))
        s1, s2 = bin_split(inv_p(pe))
        a, b = inv_s(to_int(s1), to_int(s2))
        decrypted.append(
            to_int(bin_join((to_bin(a, block_size // 2), to_bin(b, block_size // 2))))
        )
    return decrypted


def run(p, k):
    print("Plain => %s" % p)
    print("Key => %s" % k)
    keys = rnd_keys(k)
    print("Keys => %s" % keys)
    state = str_split(p)
    print("State => %s" % state)
    for b in range(len(state)):
        for i in range(cycle):
            rk = xkey(to_ord(state[b]), keys[i])
            print("Round %d => %s" % (i, rk))
            state[b] = to_chr(en(to_chr(rk)))
    print("State => %s" % state)
    return [ord(e) for es in state for e in es]


def run(c, k):
    state = str_split(to_chr(c))
    keys = rnd_keys(k)
    for b in range(len(state)):
        for i in range(cycle):
            rk = inv_en(state[b])
            # print("Round %d => %s" % (i, rk))
            state[b] = to_chr(xkey(rk, keys[i]))
    res = "".join(state)
    return res


enc = [
    8,
    167,
    8,
    118,
    243,
    40,
    84,
    118,
    208,
    133,
    241,
    141,
    136,
    170,
    225,
    118,
    201,
    117,
    121,
    218,
    208,
    218,
    201,
    40,
    70,
    133,
    68,
    133,
    208,
    214,
    113,
    189,
    12,
]
for keys in product(range(256), repeat=2):
    keys *= 4
    res = run(enc, keys)
    if res.startswith("ARA5{") and res.endswith("}"):
        print(res.encode(), keys)
        break
