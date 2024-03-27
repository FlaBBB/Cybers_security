#!/usr/bin/env python3
import sys
from math import log

from Crypto.Util.number import bytes_to_long, getPrime, isPrime
from flag import FLAG

n = pow(10, 5)
sys.setrecursionlimit(n)


def nextPrime(p):
    if isPrime(p):
        return p
    else:
        return nextPrime(p + 61)


p = getPrime(256)
q = nextPrime(nextPrime(17 * p + 1) + 3) # q > prime(17p + 1) + 3
r = nextPrime(29 * p * q) # r > prime(29pq)
s = nextPrime(q * r + p) # s > prime(qr + p)
t = nextPrime(r * s * q) # t > prime(rsq)

n = p * q * r * s * t # n = p * >(prime(17p + 1) + 3) * >(prime(29pq)) * >(prime(qr + p)) * >(prime(rsq))
e = 65537
m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)
print(f"c: {c}")
print(f"n: {n}")
