from math import ceil, sqrt
from typing import Dict


class Permutation:
    def __init__(self, mapping):
        self.length = len(mapping)

        assert set(mapping) == set(
            range(self.length)
        )  # ensure it contains all numbers from 0 to length-1, with no repetitions
        self.mapping = list(mapping)

    def __hash__(self) -> int:
        return hash(tuple(self.mapping))

    def __call__(self, *args, **kwargs):
        idx, *_ = args
        assert idx in range(self.length)
        return self.mapping[idx]

    def __mul__(self, other):
        ans = []

        for i in range(self.length):
            ans.append(self(other(i)))

        return Permutation(ans)

    def inverse(self):
        ans = [None] * self.length

        for i in range(self.length):
            ans[self(i)] = i

        return Permutation(ans)

    def __pow__(self, power, modulo=None):
        ans = Permutation.identity(self.length)
        ctr = self

        while power > 0:
            if power % 2 == 1:
                ans *= ctr
            ctr *= ctr
            power //= 2

        return ans

    def __str__(self):
        return str(self.mapping)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, Permutation)
        for x, y in zip(self.mapping, __value.mapping):
            if x != y:
                return False
        return True

    def copy(self):
        return Permutation(self.mapping.copy())

    def log(self, g: "Permutation"):  # Not Accurate
        n = ceil(sqrt(self.length))

        mul = g**n

        value: Dict[Permutation, int] = dict()
        cur = Permutation.identity(self.length)
        for i in range(n):
            if not value.get(cur):
                value[cur] = i
            cur *= mul

        cur = self.copy()
        for i in range(self.length):
            if value.get(cur):
                return n * value.get(cur) - i
            if cur == g:
                return self.length - i
            cur *= g

        return None

    @staticmethod
    def identity(length):
        return Permutation(range(length))


import random
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import unpad

g = list(range(10))
random.shuffle(g)
g = Permutation(g)

r = g**10
print(r*g.inverse()**9)
print(g)
print(g.inverse())

# with open("./output.txt", "r") as f:
#     g = f.readline().split("=")[-1].strip()
#     f.readline()
#     A = f.readline().split("=")[-1].strip()
#     f.readline()
#     B = f.readline().split("=")[-1].strip()
#     f.readline()
#     c = f.readline().split("=")[-1].strip()
#     g = eval(g)
#     A = eval(A)
#     B = eval(B)
#     c = eval(c)

# g = Permutation(g)
# A = Permutation(A)
# B = Permutation(B)

# b = B.log(g)
# print(f"{b = }")

# C = A**b

# sec = tuple(C.mapping)
# sec = hash(sec)
# sec = long_to_bytes(sec)

# hash = sha256()
# hash.update(sec)

# key = hash.digest()[16:32]
# iv = b"mg'g\xce\x08\xdbYN2\x89\xad\xedlY\xb9"

# cipher = AES.new(key, AES.MODE_CBC, iv)

# FLAG = unpad(cipher.decrypt(c))
# print(FLAG)
