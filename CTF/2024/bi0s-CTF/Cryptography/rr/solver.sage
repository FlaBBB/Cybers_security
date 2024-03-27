import logging
import sys

from Crypto.Util.number import *
from data import c1, c2, ks, n, rr
from sage.all import *
from shared.polynomial import fast_polynomial_gcd

logging.basicConfig(level=logging.DEBUG)


# https://math.stackexchange.com/questions/1863037/discrete-logarithm-modulo-powers-of-a-small-prime
def omega(x, p, e):
    numerator = (pow(x, (p - 1) * p ** (e - 1), p ** (2 * e - 1)) - 1) % p ** (
        2 * e - 1
    )
    denominator = pow(p, e)
    ans = (numerator // denominator) % p ** (e - 1)
    return ans


coeff = []
for i, k in enumerate(ks):
    base = omega(69, rr, i + 2)
    target = omega(k, rr, i + 2)
    kk = target * inverse_mod(base, rr ** (i + 1)) % rr ** (i + 1)
    coeff.append(kk)

x = PolynomialRing(Zmod(n), "x").gen()

f1 = 0
for i, k in enumerate(coeff):
    f1 += k * x**i

f1  = f1**127 - c1
f2 = x**65537 - c2
h = fast_polynomial_gcd(f1, f2)
m = -h[0] / h[1]
print(long_to_bytes(int(m)))
