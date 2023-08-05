from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.PublicKey import RSA

key = RSA.importKey(open('private.pem').read())

d = key.d
n = key.n

c = bytes_to_long(open("flag.enc", "rb").read())
M = pow(c, d, n)
print(long_to_bytes(M))