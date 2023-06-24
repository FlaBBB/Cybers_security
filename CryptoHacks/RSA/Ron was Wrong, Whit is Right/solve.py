from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, GCD
from itertools import combinations

N = []
E = []
C = []

for i in range(1, 51):
    key = RSA.import_key(open(f"src/{i}.pem").read())
    N.append(key.n)
    E.append(key.e)
    C.append(long_to_bytes(int(open(f"src/{i}.ciphertext").read(), base=16)))


cracked = dict()
for a, b in combinations(range(50), 2):
    res = GCD(N[a], N[b])
    if res != 1:
        cracked[a] = [res, N[a]//res]
        cracked[b] = [res, N[b]//res]

for c in cracked:
    phi = (cracked[c][0] - 1) * (cracked[c][1] - 1)
    d = pow(E[c], -1, phi)
    key = RSA.construct((N[c], E[c], d))
    crypto = PKCS1_OAEP.new(key)
    print(crypto.decrypt(C[c]).decode())
