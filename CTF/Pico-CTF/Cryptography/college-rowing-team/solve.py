from Crypto.Util.number import long_to_bytes
from itertools import combinations
from gmpy2 import iroot
from sympy.ntheory.modular import crt

with open('encrypted-messages.txt', 'r') as FILE:
    buffer = FILE.read().strip().split('\n\n')

for i in combinations(buffer, 3):
    N = []
    C = []
    for j in i:
        N.append(int(j.split('\n')[0].split(' ')[1]))
        C.append(int(j.split('\n')[2].split(' ')[1]))
    M, _ = crt(N, C)
    M, found = iroot(M, 3)
    if found:
        print(long_to_bytes(M))