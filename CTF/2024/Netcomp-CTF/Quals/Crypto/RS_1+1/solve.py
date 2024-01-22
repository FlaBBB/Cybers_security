from decimal import *

from Crypto.Util.number import *
from pwn import *

getcontext().prec = 100000

HOST = "103.127.99.15"
PORT = 5000

io = remote(HOST, PORT)


def get_pq(n, ppq):
    p = (Decimal(ppq) + (Decimal(ppq) ** 2 - 4 * n).sqrt()) / 2
    p = int(p)
    return p, n // p


for _ in range(30):
    n = int(io.recvline().decode().split(" = ")[1].strip())
    e = int(io.recvline().decode().split(" = ")[1].strip())
    c = int(io.recvline().decode().split(" = ")[1].strip())
    ppq = int(io.recvline().decode().split(" = ")[1].strip())
    print(f"[*] {n = }")
    print(f"[*] {e = }")
    print(f"[*] {c = }")
    print(f"[*] {ppq = }")

    p, q = get_pq(n, ppq)
    print(f"[*] {p = }")
    print(f"[*] {q = }")
    assert p * q == n
    d = inverse(e, int((p - 1) * (q - 1)))

    token = long_to_bytes(pow(c, d, n))
    io.sendline(token)
    io.recvline()

io.interactive()
