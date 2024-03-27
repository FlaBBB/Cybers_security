from hashlib import sha256
from random import shuffle

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad, unpad

# from secret import FLAG, a, b


class Permutation:
    def __init__(self, mapping):
        self.length = len(mapping)

        assert set(mapping) == set(
            range(self.length)
        )  # ensure it contains all numbers from 0 to length-1, with no repetitions
        self.mapping = list(mapping)

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

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, Permutation)
        for x, y in zip(self.mapping, __value.mapping):
            if x != y:
                return False
        return True

    def identity(length):
        return Permutation(range(length))


# x = list(range(50_000))
# shuffle(x)

# g = Permutation(x)
# print("g =", g)

# a = list(range(50_000))
# shuffle(a)
# a = Permutation(a)
# A = g * a
# print("A =", A)
# B = g**b
# print("B =", B)
with open("./output.txt", "r") as f:
    g = f.readline().split("=")[-1].strip()
    f.readline()
    A = f.readline().split("=")[-1].strip()
    f.readline()
    B = f.readline().split("=")[-1].strip()
    f.readline()
    g = eval(g)
    g = Permutation(g)
    A = eval(A)
    A = Permutation(A)
    B = eval(B)
    B = Permutation(B)

a = 839949590738986464
b = 828039274502849303
c = b"\x89\xba1J\x9c\xfd\xe8\xd0\xe5A*\xa0\rq?!wg\xb0\x85\xeb\xce\x9f\x06\xcbG\x84O\xed\xdb\xcd\xc2\x188\x0cT\xa0\xaaH\x0c\x9e9\xe7\x9d@R\x9b\xbd"

C = A**b
print(C.mapping)
# assert C.mapping == (B**a).mapping

sec = tuple(C.mapping)
sec = hash(sec)
sec = long_to_bytes(sec)

hash = sha256()
hash.update(sec)

key = hash.digest()[16:32]
iv = b"mg'g\xce\x08\xdbYN2\x89\xad\xedlY\xb9"

cipher = AES.new(key, AES.MODE_CBC, iv)

# encrypted = cipher.encrypt(pad(FLAG, 16))
# print("c =", encrypted)
FLAG = cipher.decrypt(c)
print(FLAG)
