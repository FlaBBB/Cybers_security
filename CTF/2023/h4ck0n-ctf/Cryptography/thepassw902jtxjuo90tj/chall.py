from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Util.Padding import pad, unpad

# how about 2 part flags
flag1 = b"FLAG PART 1 HEHEHE"
flag2 = b"FLAG PART 2 not hehe :("

flagnum = bytes_to_long(flag1)
flagnum2 = bytes_to_long(pad(flag2, 256))

assert len(bin(flagnum)[2:]) == 303

p = getPrime(2048)
q = getPrime(2048)
N = p * q
e = 65537

# p isn't needed anymore; must be corrupted
p = p^flagnum
print("masked_p={}".format(hex(p)))
print("N={}\ne={}".format(hex(N), hex(e)))

ct = pow(flagnum2, e, N)
print("ct={}".format(hex(ct)))