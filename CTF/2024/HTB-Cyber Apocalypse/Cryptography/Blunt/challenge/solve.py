import random
from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad
from sage.all import *

iv = b"\xc1V2\xe7\xed\xc7@8\xf9\\\xef\x80\xd7\x80L*"
p = 0xDD6CC28D
g = 0x83E21C05
A = 0xCFABB6DD
B = 0xC4A21BA9
ciphertext = b"\x94\x99\x01\xd1\xad\x95\xe0\x13\xb3\xacZj{\x97|z\x1a(&\xe8\x01\xe4Y\x08\xc4\xbeN\xcd\xb2*\xe6{"

K = Zmod(p)
G = K(g)

b = discrete_log(Integer(B), G)
# print(b)

C = pow(A, b, p)

hash = sha256()
hash.update(long_to_bytes(C))

key = hash.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)

print(cipher.decrypt(ciphertext))
