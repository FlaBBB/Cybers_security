from math import isqrt
from gmpy2 import iroot
from pwn import *

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

def modeA(N, c):
    e = 65537
    phi = N - 1
    d = pow(e, -1, phi)
    return pow(c, d, N)

def modeB(N, c):
    m = iroot(c, 3)
    while not m[1]:
        c += N
        m = iroot(c, 3)
    return m[0]

def modeC(N, c):
    e = 65537
    p, q = factorize(N)
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return pow(c, d, N)

HOST = "34.101.174.85"
PORT = 10004

io = connect(HOST, PORT)
io.recvline()

for i in range(1, 101):
    try:
        mode = io.recvline().decode().strip()
        mode = mode.split(" = ")[1]
    except IndexError:
        print(mode)
        break
    n = int(io.recvline().decode().strip().split(" = ")[1])
    c = int(io.recvlines(2)[1].decode().strip().split(" = ")[1])
    print(f"Round {i}")
    print(f"Mode: {mode}")
    print(f"N: {n}")
    print(f"C: {c}")
    if mode == "A":
        m = modeA(n, c)
    elif mode == "B":
        m = modeB(n, c)
    elif mode == "C":
        m = modeC(n, c)
    print(f"got M: {m}")
    print()
    io.sendlineafter(b": ", str(m).encode())
    if "Correct!" not in io.recvline().decode():
        break
io.interactive()