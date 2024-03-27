import string
from itertools import product

from aes import AES
from pwn import *
from sage.all import *

HOST = "localhost"
PORT = 10121

io = remote(HOST, PORT)

do_nothing = lambda *x: None

flag_dict = string.ascii_letters + string.digits + "_"


def get(io: remote, opt: bytes, sopt: bytes):
    data = b""
    if sopt != b"secret":
        data = sopt
        sopt = b"data"
    io.sendlineafter(b"> ", opt + b" " + sopt + b" " + data.hex().encode())
    return bytes.fromhex(io.recvline().strip().decode())


def no_ark(ct: bytes):
    c = AES(b"a" * 16)
    c._add_round_key = lambda *x: None
    return c.decrypt(ct)


def no_sb(ct: bytes, p2: bytes, ct2: bytes):
    def bytes2mat(b):
        a = []
        for i in b:
            tmp = bin(i)[2:].zfill(8)
            for j in tmp:
                a.append(int(j))
        return Matrix(GF(2), a)

    def mat2bytes(m):
        a = ""
        for i in range(128):
            a += str(m[0, i])
        a = [a[i : i + 8] for i in range(0, 128, 8)]
        a = [int(i, 2) for i in a]
        return bytes(a)

    I = identity_matrix(GF(2), 8)
    X = Matrix(GF(2), 8, 8)
    for i in range(7):
        X[i, i + 1] = 1
    X[3, 0] = 1
    X[4, 0] = 1
    X[6, 0] = 1
    X[7, 0] = 1

    C = block_matrix(
        [[X, X + I, I, I], [I, X, X + I, I], [I, I, X, X + I], [X + I, I, I, X]]
    )

    zeros = Matrix(GF(2), 8, 8)
    zeros2 = Matrix(GF(2), 32, 32)
    o0 = block_matrix(
        [
            [I, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
        ]
    )

    o1 = block_matrix(
        [
            [zeros, zeros, zeros, zeros],
            [zeros, I, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
        ]
    )

    o2 = block_matrix(
        [
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, I, zeros],
            [zeros, zeros, zeros, zeros],
        ]
    )

    o3 = block_matrix(
        [
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, zeros],
            [zeros, zeros, zeros, I],
        ]
    )

    S = block_matrix(
        [[o0, o1, o2, o3], [o3, o0, o1, o2], [o2, o3, o0, o1], [o1, o2, o3, o0]]
    )

    M = block_matrix(
        [
            [C, zeros2, zeros2, zeros2],
            [zeros2, C, zeros2, zeros2],
            [zeros2, zeros2, C, zeros2],
            [zeros2, zeros2, zeros2, C],
        ]
    )

    R = M * S
    A = S * (R**9)

    p2 = bytes2mat(p2).transpose()
    ct2 = bytes2mat(ct2).transpose()

    K = ct2 - A * p2
    return mat2bytes((A.inverse() * (bytes2mat(ct).transpose() - K)).transpose())


def no_sr(ct: bytes):
    global io
    _ct = [ct[i : i + 4] for i in range(0, len(ct), 4)]
    res = [0 in range(4)]
    for _ in range(4):
        try:
            f = product(flag_dict, repeat=4).encode()
            e = get(io, b"sr", f * 4)
            if e[:4] in _ct:
                off = _ct.index(e[:4])
                res[off] = e[4:]
                if 0 not in res:
                    break
        except EOFError:
            io = remote(HOST, PORT)
            continue
    return b"".join(res)


def no_mc(ct: bytes):
    relation = [0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 5, 14, 7]

    c = AES(os.urandom(16))
    c._mix_columns = do_nothing

    lookup = [{} for _ in range(16)]
    for i in range(256):
        ptest = bytes([i] * 16)
        ctest = c.encrypt(ptest)
        for j in range(16):
            lookup[j][ctest[j]] = i

    recovered = ["??" for _ in range(16)]
    for i in range(16):
        recovered[i] = lookup[relation[i]][ct[relation[i]]]

    return b"".join([bytes([i]) for i in recovered])


flag = b""
ct_sb = get(io, b"sb", b"secret")
flag += no_sb(ct_sb, b"a" * 16, get(io, b"sb", b"a" * 16))

ct_sr = get(io, b"sr", b"secret")
flag += no_sr(ct_sr)

ct_mc = get(io, b"mc", b"secret")
flag += no_mc(ct_mc)

ct_ark = get(io, b"ark", b"secret")
flag += no_ark(ct_ark)

print(flag)
