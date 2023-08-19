import string
import random
from pwn import *

DICT1 = [i for i in string.digits + string.ascii_uppercase]

def gen_key():
    key = ["A"] * 24

    for i in range(4, 24, 5):
        key[i] = "-"

    for k in range(0, 24, 5):
        for l in range(k, k + 4):
            key[l] = random.choice(DICT1)

    return "".join(key)

HOST = "34.101.174.85"
PORT = 10003

io = connect(HOST, PORT)

for _ in range(100):
    io.sendlineafter(b"> ", gen_key().encode())
io.interactive()