import os

from aes import AES
from sage.all import *

do_nothing = lambda *x: None


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
A = S * (
    R**9
)  # sorry for the inconsistency in the variable name, this is supposed to be SA^9 that I talked about

c = AES(os.urandom(16))
c._sub_bytes = do_nothing
p = b"Very secret text"
ct = c.encrypt(p)
p2 = b"Known plaintextt"
ct2 = c.encrypt(p2)

p2 = bytes2mat(p2).transpose()
ct2 = bytes2mat(ct2).transpose()

K = ct2 - A * p2
recovered_plaintext = mat2bytes(
    (A.inverse() * (bytes2mat(ct).transpose() - K)).transpose()
)
print(recovered_plaintext)
