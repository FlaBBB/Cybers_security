import os
import sys
from math import gcd

from Crypto.Util.number import *
from pwn import *

path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
)
if sys.path[1] != path:
    sys.path.insert(1, path)

from attacks.rsa import low_exponent
from shared.crt import fast_crt


def attack(N, e, c):
    """
    Recovers the plaintext from e ciphertexts, encrypted using different moduli and the same public exponent.
    :param N: the moduli
    :param e: the public exponent
    :param c: the ciphertexts
    :return: the plaintext
    """
    assert e == len(N) == len(c), "The amount of ciphertexts should be equal to e."

    for i in range(len(N)):
        for j in range(len(N)):
            if i != j and gcd(N[i], N[j]) != 1:
                raise ValueError(
                    f"Modulus {i} and {j} share factors, Hastad's attack is impossible."
                )

    c, _ = fast_crt(c, N)
    return low_exponent.attack(e, c)


# nc 13.127.242.3 3211
HOST = "65.0.128.220"
PORT = 31363

io = remote(HOST, PORT)

# context.log_level = "DEBUG"

io.recvuntil(b"n = ")
n = eval(io.recvline().strip().decode())
io.recvuntil(b"c = ")
c = eval(io.recvline().strip().decode())
io.recvuntil(b"e = ")
e = int(io.recvline().strip().decode())

m = attack(n, e, c)
for _n, _c in zip(n, c):
    assert pow(m, e, _n) == _c
io.sendlineafter(b": ", str(m).encode())
log.success(f"m = {str(m)}")

io.interactive()
