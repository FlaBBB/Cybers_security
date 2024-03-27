import os

from Crypto.Util.number import *
from pwn import *
from tea import TEA

f = 1 << 31
forger1 = f | (f << 32)
forger2 = (f << (32 * 2)) | (f << (32 * 3))

iv = bytes.fromhex("0dddd2773cf4b908")
# print(hex(f))

m = bytes.fromhex("0f7ebf6b1ef7d7ff0a07603d85c10a84e6985b0f")
c = bytes.fromhex("79267c0722416bc0a60b89880bb3b926c61a12ee839363df")

key = b"\x00" * 16
# print(key.hex())
cipher = TEA(key)
_c = cipher.encrypt(m)
# print(_c.hex())

_m = cipher.decrypt(c)
# print(_m.hex())
iv = xor(_m[:8], m[:8])
print(iv.hex())
