from Crypto.Util.number import long_to_bytes
from decimal import *
getcontext().prec = 1000

n = 742449129124467073921545687640895127535705902454369756401331
e = 3
ct = 39207274348578481322317340648475596807303160111338236677373

# factorize with yafu
p = 986369682585281993933185289261
q = 752708788837165590355094155871

phi = (p-1)*(q-1)

d = pow(e, -1, phi)

M = pow(ct, d, n)

decrypted = long_to_bytes(M)
print(decrypted)

