# https://cr.yp.to/snuffle/spec.pdf

import struct


def xor_bytes(b0, b1):
    return bytes(a ^ b for a, b in zip(b0, b1))


BLOCKSIZE = 4 * 4 * 4


def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


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
    c = struct.unpack("<II", counter)
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


def blockcount(b):
    return ((len(b) - 1) // BLOCKSIZE) + 1


def nthblock(b, n):
    return b[BLOCKSIZE * n : BLOCKSIZE * (n + 1)]


def encrypt(key, nonce, pt):
    out = b""
    for i in range(blockcount(pt)):
        out += xor_bytes(
            salsa20_block(key, nonce, struct.pack(">Q", i)), nthblock(pt, i)
        )
    return out


def decrypt(key, nonce, ct):
    return encrypt(key, nonce, ct)


def test():
    key = b"x" * 32
    nonce = b"x" * 8
    print(salsa20_block(key, nonce, struct.pack(">Q", 0)))
    print(len(salsa20_block(key, nonce, struct.pack(">Q", 0))))
    print(
        len("THIS IS A REALLY IMPORTANT MESSAGE, TOP SECRET, DESTROY AFTER RECEIVING: ")
    )
    # pt = b'1234' * 64 + b'0'
    # enc = encrypt(bytes([0] * 32), bytes([0] * 8), pt)
    # dec = decrypt(bytes([0] * 32), bytes([0] * 8), enc)

    # assert dec == pt


def main():
    test()

    # from secrets import token_bytes

    # from secret import FLAG, KEY

    # pt = 'THIS IS A REALLY IMPORTANT MESSAGE, TOP SECRET, DESTROY AFTER RECEIVING: '

    # print(encrypt(KEY, token_bytes(8), (pt + FLAG).encode()).hex())


if __name__ == "__main__":
    main()
