from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

FLAG = b"crypto{n0n_574nd4rd_p4d_c0n51d3r3d_h4rmful}"


def pad100(msg):
    return msg + b'\x01' * (100 - len(msg))


key = RSA.generate(1024, e=3)
n, e = key.n, key.e

m = bytes_to_long(pad100(FLAG))
c = pow(m, e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")

# ct = pow(flag*p, e, n)
# ct = (pow(flag, e, n) * pow(p, e, n)) % n
# pow(flag, 3, n) = (pow(flag, e, n) * pow(p, e, n) * pow(p, -e, n)) % n
#                 = (ct * pow(p, -e, n)) % n

c2 = pow(bytes_to_long(FLAG), e, n) * pow(2, 8 * (100 - len(FLAG)) * e, n)
for i in range(100 - len(FLAG)):
    c2 += 0x01 * pow(2, 8 * i, n)
c2 %= n

print(f"c2 = {c2}")