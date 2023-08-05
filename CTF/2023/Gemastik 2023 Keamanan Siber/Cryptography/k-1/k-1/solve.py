from pwn import *
from sympy import symbols, solve, Eq
import sys

sys.set_int_max_str_digits(1000000)

io = connect("ctf-gemastik.ub.ac.id", 10000)

k = int(io.recvline().decode().split(" = ")[1].strip())

shared = eval("[" + io.recvuntil(b"password: ").replace(b"password: ", b"").decode().strip().replace("\n", ",") + "]")

with open("shared.txt", "w") as f:
    f.write(str(shared))

coeffs = [symbols("pass")]
for i in range(k - 1):
    coeffs.append(symbols(f"coeffs_{i}"))

EQ = []
for b in shared:
    x, y = b
    EQ.append(Eq(sum(map(lambda i : coeffs[i] * pow(x, i), range(k))), y))

solution = solve(EQ, [coeffs[0]])

print(solution)