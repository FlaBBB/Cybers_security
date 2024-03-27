from hashlib import sha256
from typing import List, Tuple

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad
from sage.all import *
from sage.arith.functions import LCM_list
from sage.arith.misc import CRT_list


def permutation_identity(n):
    return Permutation(vector(range(n)) + vector([1] * n))


def convert_to_permutation(l):
    return Permutation(vector(l) + vector([1] * len(l)))


def permutation_pow_fast(g: Permutation, n):
    g_cycle: List[Tuple[int]] = g.cycle_tuples()
    ans = [0] * g.size()
    for cycle in g_cycle:
        p = n % len(cycle)
        for i in range(len(cycle)):
            ans[cycle[i] - 1] = cycle[(i + p) % len(cycle)]
    return Permutation(ans)


def max_cycle_permutation(p: Permutation):
    cycles = p.cycle_tuples()
    g_cycle_mod = list(map(lambda x: len(x), cycles))
    return LCM_list(g_cycle_mod) + 1


def log_fast(r: Permutation, g: Permutation):
    g_cycle: List[Tuple[int]] = g.cycle_tuples()
    g_cycle_mod = list(map(lambda x: len(x), g_cycle))
    remainder = []
    for cycle in g_cycle:
        c = cycle[0]
        remainder.append(cycle.index(r[c - 1]) % len(cycle))
    res = CRT_list(remainder, g_cycle_mod)
    return res % max_cycle_permutation(g)


with open("./challenge/output.txt", "r") as f:
    g = f.readline().split("=")[-1].strip()
    f.readline()
    A = f.readline().split("=")[-1].strip()
    f.readline()
    B = f.readline().split("=")[-1].strip()
    f.readline()
    g = eval(g)
    A = eval(A)
    B = eval(B)

g = convert_to_permutation(g)
A = convert_to_permutation(A)
B = convert_to_permutation(B)

a = log_fast(A, g)
print(f"{a = }")
b = log_fast(B, g)
print(f"{b = }")
C = permutation_pow_fast(B, a)
assert permutation_pow_fast(g, a) == A
assert permutation_pow_fast(g, b) == B
assert C == permutation_pow_fast(A, b)

sec = tuple(map(lambda x: x - 1, C))
sec = hash(sec)
sec = long_to_bytes(sec)

hash = sha256()
hash.update(sec)

key = hash.digest()[16:32]
iv = b"mg'g\xce\x08\xdbYN2\x89\xad\xedlY\xb9"

cipher = AES.new(key, AES.MODE_CBC, iv)

c = b"\x89\xba1J\x9c\xfd\xe8\xd0\xe5A*\xa0\rq?!wg\xb0\x85\xeb\xce\x9f\x06\xcbG\x84O\xed\xdb\xcd\xc2\x188\x0cT\xa0\xaaH\x0c\x9e9\xe7\x9d@R\x9b\xbd"
FLAG = cipher.decrypt(c)
FLAG = unpad(FLAG, 16)
print(FLAG)
