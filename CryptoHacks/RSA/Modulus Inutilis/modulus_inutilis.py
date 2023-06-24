from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

e = 3
d = -1

while d == -1:
    p = getPrime(1024)
    q = getPrime(1024)
    phi = (p - 1) * (q - 1)
    try:
        d = inverse(e, phi)
    except:
        continue

n = p * q

flag = b"XXXXXXXXXXXXXXXXXXXXXXX"
pt = bytes_to_long(flag)
ct = pow(pt, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"ct = {ct}")
print(f"p = {p}")
print(f"q = {q}")

pt = pow(ct, d, n)
decrypted = long_to_bytes(pt)
assert decrypted == flag