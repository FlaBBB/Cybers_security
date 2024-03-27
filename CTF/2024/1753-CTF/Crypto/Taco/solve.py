import struct
from pwn import xor

def xor_bytes(b0, b1):
    return bytes(a ^ b for a, b in zip(b0, b1))


def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def quarterround(state, indexes):
    state[indexes[1]] ^= rotl((state[indexes[0]] + state[indexes[3]]) & 0xFFFFFFFF, 7)
    state[indexes[2]] ^= rotl((state[indexes[1]] + state[indexes[0]]) & 0xFFFFFFFF, 9)
    state[indexes[3]] ^= rotl((state[indexes[2]] + state[indexes[1]]) & 0xFFFFFFFF, 13)
    state[indexes[0]] ^= rotl((state[indexes[3]] + state[indexes[2]]) & 0xFFFFFFFF, 18)


def rowround(state):
    quarterround(state, [0, 1, 2, 3])
    quarterround(state, [5, 6, 7, 4])
    quarterround(state, [10, 11, 8, 9])
    quarterround(state, [15, 12, 13, 14])


def columnround(state):
    quarterround(state, [0, 4, 8, 12])
    quarterround(state, [5, 9, 13, 1])
    quarterround(state, [10, 14, 2, 6])
    quarterround(state, [15, 3, 7, 11])


def doubleround(state):
    columnround(state)
    rowround(state)


def salsa20_block(key, nonce, counter):
    k = struct.unpack("<IIIIIIII", key)
    n = struct.unpack("<II", nonce)
    c = struct.unpack("<II", struct.pack("<Q", counter))
    e = struct.unpack("<IIII", b"expand 32-byte k")
    state = [
        e[0],
        k[0],
        k[1],
        k[2],
        k[3],
        e[1],
        n[0],
        n[1],
        c[0],
        c[1],
        e[2],
        k[4],
        k[5],
        k[6],
        k[7],
        e[3],
    ]
    for i in range(10):
        doubleround(state)

    return struct.pack("<" + "I" * 16, *state)


def dequarterround(state, indexes):
    state[indexes[0]] ^= rotl((state[indexes[3]] + state[indexes[2]]) & 0xFFFFFFFF, 18)
    state[indexes[3]] ^= rotl((state[indexes[2]] + state[indexes[1]]) & 0xFFFFFFFF, 13)
    state[indexes[2]] ^= rotl((state[indexes[1]] + state[indexes[0]]) & 0xFFFFFFFF, 9)
    state[indexes[1]] ^= rotl((state[indexes[0]] + state[indexes[3]]) & 0xFFFFFFFF, 7)


def derowround(state):
    dequarterround(state, [15, 12, 13, 14])
    dequarterround(state, [10, 11, 8, 9])
    dequarterround(state, [5, 6, 7, 4])
    dequarterround(state, [0, 1, 2, 3])


def decolumnround(state):
    dequarterround(state, [15, 3, 7, 11])
    dequarterround(state, [10, 14, 2, 6])
    dequarterround(state, [5, 9, 13, 1])
    dequarterround(state, [0, 4, 8, 12])


def dedoubleround(state):
    derowround(state)
    decolumnround(state)


def salsa20_block_back(rkey):
    state = list(struct.unpack("<IIIIIIIIIIIIIIII", rkey))
    for i in range(10):
        dedoubleround(state)

    k = struct.pack(
        "<IIIIIIII",
        state[1],
        state[2],
        state[3],
        state[4],
        state[11],
        state[12],
        state[13],
        state[14],
    )
    n = struct.pack("<II", state[6], state[7])
    c = struct.pack("<II", state[8], state[9])
    return k, n, struct.unpack("<Q", c)


c = open("taco_encrypted", "r").read()
c = bytes.fromhex(c)
pt = b'THIS IS A REALLY IMPORTANT MESSAGE, TOP SECRET, DESTROY AFTER RECEIVING: '

rkey0 = xor(pt[:64], c[:64])
k, n, c = salsa20_block_back(rkey0)
print(k, n, c)