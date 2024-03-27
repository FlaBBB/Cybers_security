from sage.all import *


# Lifts a point to the p-adic numbers.
def _lift(E, P, gf):
    x, y = map(ZZ, P.xy())
    for point_ in E.lift_x(x, all=True):
        _, y_ = map(gf, point_.xy())
        if y == y_:
            return point_


def attack(G, P):
    """
    Solves the discrete logarithm problem using Smart's attack.
    More information: Smart N. P., "The discrete logarithm problem on elliptic curves of trace one"
    :param G: the base point
    :param P: the point multiplication result
    :return: l such that l * G == P
    """
    E = G.curve()
    gf = E.base_ring()
    p = gf.order()
    assert E.trace_of_frobenius() == 1, f"Curve should have trace of Frobenius = 1."

    E = EllipticCurve(
        Qp(p), [int(a) + p * ZZ.random_element(1, p) for a in E.a_invariants()]
    )
    G = p * _lift(E, G, gf)
    P = p * _lift(E, P, gf)
    Gx, Gy = G.xy()
    Px, Py = P.xy()
    return int(gf((Px / Py) / (Gx / Gy)))


from Crypto.Util.number import long_to_bytes
from pwn import *

# nc 143.47.53.106 34871
HOST = "143.47.53.106"
PORT = 34871

io = remote(HOST, PORT)

p = 0xA15C4FB663A578D8B2496D3151A946119EE42695E18E13E90600192B1D0ABDBB6F787F90C8D102FF88E284DD4526F5F6B6C980BF88F1D0490714B67E8A2A2B77
a = 0x5E009506FCC7EFF573BC960D88638FE25E76A9B6C7CAEEA072A27DCD1FA46ABB15B7B6210CF90CABA982893EE2779669BAC06E267013486B22FF3E24ABAE2D42
b = 0x2CE7D1CA4493B0977F088F6D30D9241F8048FDEA112CC385B793BCE953998CAAE680864A7D3AA437EA3FFD1441CA3FB352B0B710BB3F053E980E503BE9A7FECE
E = EllipticCurve(GF(p), [a, b])
n = E.order()
assert n == p

log.info(f"p = {p}")
log.info(f"a = {a}")
log.info(f"b = {b}")
log.info(f"n = {n}")

G = E.random_point()

x, y = G.xy()

log.info(f"g.x = {x}")
log.info(f"g.y = {y}")

io.sendline(str(p).encode())
io.sendline(str(a).encode())
io.sendline(str(b).encode())
io.sendline(str(x).encode())
io.sendline(str(y).encode())
io.sendline(str(n).encode())

io.recvuntil(b"g*x: ")

Sx, Sy = io.recvline().strip().decode().split(", ")
S = E(Sx, Sy)

log.info(f"S.x = {Sx}")
log.info(f"S.y = {Sy}")

log.info(f"Attacking S...")
s = attack(G, S)
log.success(f"Found s = {s}")
io.sendlineafter(b"what's x?: ", str(s).encode())

io.recvuntil(b"Here's your flag: ")

Fx, Fy = io.recvline().strip().decode().split(", ")
F = E(Fx, Fy)

log.info(f"F.x = {Fx}")
log.info(f"F.y = {Fy}")

flag = attack(G, F)
log.success(f"Found f = {s}")
print(long_to_bytes(flag))
