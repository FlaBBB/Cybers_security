from Crypto.Util.number import *
from sympy.ntheory.modular import crt
from math import gcd
from pwn import *
import gmpy2

# nc 34.101.122.7 10004
HOST = "34.101.122.7"
PORT = 10004

def get_encrypt(io, e):
    io.sendlineafter(b">> ", b"1")
    io.sendlineafter(b"Enter your public exponent (e cannot be 1 and even): ", str(e).encode())
    temp = io.recvline()
    return int(temp.split(b": ")[1])

def recover_modulus(io, encrypt):
    C = []
    e = 3
    for _ in range(3):
        C.append(encrypt(io, e))
        e *= 3
    
    c_m1 = C[0] ** 3
    c_m2 = C[1] ** 3
    
    n = gcd(c_m1 - C[1], c_m2 - C[2])
    while n % 2 == 0:
        n //= 2
    return n, C[0] 

def main_attack():
    N = []
    C = []
    e = 3
    for _ in range(3):
        io = remote(HOST, PORT)
        n, c = recover_modulus(io, get_encrypt)
        N.append(n)
        C.append(c)
        io.close()
    m = crt(N, C)[0]
    m = gmpy2.iroot(m, 3)[0]
    print(long_to_bytes(m))


main_attack()