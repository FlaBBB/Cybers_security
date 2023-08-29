

# This file was *autogenerated* from the file /mnt/d/Programming/Cyber Security/CryptoHacks/RSA/Bespoke Padding/solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_13386 = Integer(13386)
from pwn import *
import json

def gcd(a, b): 
    while b:
        a, b = b, a % b
    return a.monic()

def franklinreiter(C1, C2, e, N, a, b):
    P = PolynomialRing(Zmod(N), names=('X',)); (X,) = P._first_ngens(1)
    g1 = (a*X + b)**e - C1
    g2 = X**e - C2
    result = -gcd(g1, g2).coefficients()[_sage_const_0 ]
    return hex(int(result))[_sage_const_2 :].replace("L","").decode("hex")

# nc socket.cryptohack.org 13386
io = remote("socket.cryptohack.org", _sage_const_13386 )

io.sendlineafter(b"flag.", b"{\"option\": \"get_flag\"}")
rec = io.recvline()
print(rec)

