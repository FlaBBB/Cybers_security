from Crypto.Util.number import *
from math import isqrt
from gmpy2 import iroot
from pwn import *

# nc 0x7e7ctf.zerobyte.me 10021
HOST = "0x7e7ctf.zerobyte.me"
PORT = 10021

def is_square(x):
    """
    Returns the square root of x if x is a perfect square, or None otherwise.
    :param x: x
    :return: the square root of x or None
    """
    y = isqrt(x)
    return y if y ** 2 == x else None

def factorize(N):
    """
    Recovers the prime factors from a modulus using Fermat's factorization method.
    :param N: the modulus
    :return: a tuple containing the prime factors, or None if the factors were not found
    """
    a = isqrt(N)
    b = a * a - N
    while b < 0 or not is_square(b):
        a += 1
        b = a * a - N

    p = a - isqrt(b)
    q = N // p
    if p * q == N:
        return p, q

io = remote(HOST, PORT)

for _ in range(100):
    n = int(io.recvline().decode().strip().split(" = ")[1])
    e = int(io.recvline().decode().strip().split(" = ")[1])
    c = int(io.recvline().decode().strip().split(" = ")[1])

    p, q = factorize(n)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)

    token = long_to_bytes(m)

    io.sendlineafter(b"[TOKEN]>", token)
    io.recvline()
io.interactive()