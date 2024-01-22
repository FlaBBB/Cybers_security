#!/usr/bin/env sage

from Crypto.Util.number import *

# from flag import flag

F, k = GF(2**8), 14

while True:
    G = random_matrix(F, k)
    if G.is_invertible():
        break

# flag = flag.lstrip(b"MAPNA{").rstrip(b"}")
# m = bytes_to_long(flag)
# H = G**m

H = G**1000

print(f"G = {G.list()}")
print(f"H = {H.list()}")
