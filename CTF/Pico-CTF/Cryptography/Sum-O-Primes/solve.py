from sympy import symbols, Eq, solve
from Crypto.Util.number import long_to_bytes

with open("output.txt", 'r') as FILE:
    buffer = FILE.read().splitlines()

x = int(buffer[0].split(' = ')[1], 16)
n = int(buffer[1].split(' = ')[1], 16)
c = int(buffer[2].split(' = ')[1], 16)
e = 65537

p, q = symbols('p q')

eq1 = Eq(p + q, x)
eq2 = Eq(p * q, n)

p, q = solve((eq1, eq2), (p, q))[0]

phi = (p - 1) * (q - 1)
d = pow(e, -1, int(phi))

M = pow(c, d, n)

print("Flag: " + long_to_bytes(M).decode("utf-8"))