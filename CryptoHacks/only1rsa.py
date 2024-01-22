import random
import string

from Crypto.Util.number import *

bits = 512


def get_random_string(bit: int):
    return "".join(random.choice(string.ascii_letters) for _ in range(bit // 8))


p, q, r, s = getPrime(bits), getPrime(bits), getPrime(bits), getPrime(bits)
n = p * q * r * s

e = 65537

m = get_random_string(bits)

m = bytes_to_long(m.encode())
assert m.bit_length() < bits
print(m.bit_length())

c = pow(m, e, n)

_m = pow(c, inverse(e, p - 1), p)
assert _m == m
_m = long_to_bytes(_m)

print(f"{_m = }")
