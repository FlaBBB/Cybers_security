from Crypto.Util.number import *
from pwn import xor
import string
import itertools

def combine(a, b):
    for x in a:
        for y in b:
            yield x + y

readable = string.ascii_letters + string.digits + string.punctuation + " "

database = open("database.txt", "r").readlines()
database = list(map(lambda x: bytes.fromhex(x.strip()), database))

c1 = bytes.fromhex("c1229ab7b6350824f2dc11e8510fc249ad48") # take cipher that seems to be the same length
c2 = bytes.fromhex("d52b94abaa350824f2dc11e8510fc249ad48")

attack = xor(c1, c2).strip(b"\x00")

possible_m1 = []
possible_m2 = []
for i, att in enumerate(attack):
    possible_m1.append([])
    possible_m2.append([])
    for r in readable:
        res = chr(att ^ ord(r))
        if res in readable:
            possible_m1[i].append(r)
            possible_m2[i].append(r)

m1 = None
for p in possible_m1:
    if m1 is None:
        m1 = p
    else:
        m1 = combine(m1, p)

m2 = None
for p in possible_m2:
    if m2 is None:
        m2 = p
    else:
        m2 = combine(m2, p)

for a,b in zip(m1, m2):
    print(a, b)