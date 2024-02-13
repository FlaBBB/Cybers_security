import math

# from secret import flag, p, q
from math import gcd

from Crypto.Util.number import *
from gmpy2 import next_prime

# m = bytes_to_long(flag.encode())
p = getPrime(1024)
q = getPrime(1024)
n = p * q


power1 = getPrime(128)
power2 = getPrime(128)
out1 = pow((p + 5 * q), power1, n)
out2 = pow((2 * p - 3 * q), power2, n)
eq1 = next_prime(out1)

# c = pow(m, eq1, n)


# with open("chall2.txt", "w") as f:
#     f.write(f"power1={power1}\npower2={power2}\neq1={eq1}\nout2={out2}\nc={c}\nn={n}")

# out1 = (p + 5q)^power1 mod n
# out2 = (2p - 3q)^power2 mod n

g = (2 * out1 - out2) % n

# g = (2 * (p + 5 * q)^power1 - (2 * p - 3 * q)^power2) % n
# 

print(gcd(g, n))
