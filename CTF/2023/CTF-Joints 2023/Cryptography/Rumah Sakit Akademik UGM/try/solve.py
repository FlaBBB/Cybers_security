
import functools
from pwn import binascii
from Crypto.Util.number import inverse
import re

def chinese_remainder(n, a):
    sum = 0
    prod = functools.reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * inverse(p, n_i) * p
    return sum % prod

def inv_pow(c, e):
    low = -1
    high = c+1
    while low + 1 < high:
        m = (low + high) // 2
        p = pow(m, e)
        if p < c:
            low = m
        else:
            high = m
    m = high
    assert pow(m, e) == c
    return m

flag = open("flag.enc").read().split("\n\n")
e = int(re.search(f"e:\d+", flag[0]).group()[2:])

N = [int(re.search(f"n:\d+", n).group()[2:]) for n in flag if n not in ["","\n"]]
C = [int(re.search(f"n:\d+", c).group()[2:]) for c in flag if c not in ["","\n"]]


print(len(N))
# a = chinese_remainder(N, C)
# for n, c in zip(N, C):
#     assert a % n == c
# m = inv_pow(a, e)
# print(binascii.unhexlify(hex(m)[2:]).decode())