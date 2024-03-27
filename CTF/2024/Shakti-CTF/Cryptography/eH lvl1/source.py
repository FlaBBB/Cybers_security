from Crypto.Util.number import *
from gmpy2 import *
from secret import b, d, e, hint, msg

p = getPrime(512)
q = getPrime(512)
n = p * q
m = bytes_to_long(msg)
h = bytes([i ^ b for i in hint])
print(f"h = {hex(bytes_to_long(h))}")
ct = pow(m, e, n)
de = pow(ct, d, n)
assert m == de
print("ct = ", ct)
print("p = ", p)
print("q = ", q)
