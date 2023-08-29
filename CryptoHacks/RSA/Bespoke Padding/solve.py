from pwn import *
from sage.all import *
import json

def gcd(a, b): 
    while b:
        a, b = b, a % b
    return a.monic()

def franklinreiter(C1, C2, e, N, a1, a2, b1, b2):
    P = PolynomialRing(Zmod(N), names=('X',))
    (X,) = P._first_ngens(1)
    g1 = (a1*X + b1)**e - C1
    g2 = (a2*X + b2)**e - C2
    result = -gcd(g1, g2).coefficients()[0]
    return bytes.fromhex(hex(int(result))[2:].replace("L",""))

def get_flag(io):
    io.sendline(b"{\"option\": \"get_flag\"}")
    rec = b""
    while not rec or rec == b"\n":
        rec = io.recvline()
    rec = json.loads(rec)
    return rec

# nc socket.cryptohack.org 13386
io = remote("socket.cryptohack.org", 13386)
io.recvuntil(b"flag.")

e = 11

rec = get_flag(io)
N = rec["modulus"]

C1 = rec["encrypted_flag"]
a1, b1 = rec["padding"]

rec = get_flag(io)
C2 = rec["encrypted_flag"]
a2, b2 = rec["padding"]

flag = franklinreiter(C1, C2, e, N, a1, a2, b1, b2)
print(flag)