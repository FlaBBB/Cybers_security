from sage import *

list_char_flag = "4YV2uI0dyTWU6x8wF3DEXM_s-oqZkORmaHgvA{pCGJel1ncQzNSKbP?9j75ih}rBfLt"

def find(char, lis):
    for i, l in enumerate(lis):
        if l == char:
            return i
    return -1

def encode(s):
    res = list(map(lambda c: find(c, list(list_char_flag)), list(s)))
    return res

def decode(l):
    res = list(map(lambda x: list_char_flag[x], l))
    return "".join(res)

def encrypt(a, b):
    return a * b % 67

def decrypt(c, b):
    return b.solve_left(c) % 67

key = "3RgJFzNJq6Pxxc7L1LjDtTtPA2q?vhw1JUF_}oBBxi3hid_vpSxpMyrKdS{J9qbia7S"
cipher = "7ETBZhbt_XhnStCIlf1vbq7o-QDUR0aTLX_vFJxx{90pyHvdHhHh?pG-eIj3ao98"

_b = encode(key)
b = Matrix([_b[i:i+8] for i in range(0,8^2,8)])
C = encode(cipher)

A = []
for i in range(0, len(C), 8):
    c = Matrix([C[i:i+8]])
    A += decrypt(c, b).list()
print(decode(A))