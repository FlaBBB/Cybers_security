from hashlib import sha256
from itertools import product

from pwn import *

# nc mc.ax 31001
HOST = "mc.ax"
PORT = 31001


def hash(x, n):
    for _ in range(n):
        x = sha256(x).digest()
    return x


def check_msg(msg1: bytes, msg2: bytes):
    if msg1 == msg2:
        return
    h_msg1, h_msg2 = hash(msg1, 1), hash(msg2, 1)
    left_hand = 0
    score = 0
    for h1, h2 in zip(h_msg1, h_msg2):
        if left_hand == 0:
            left_hand = 1 if h1 > h2 else -1
        elif left_hand == -1 and h1 > h2:
            left_hand = -2
        elif left_hand == 1 and h1 < h2:
            left_hand = -2
        score += h2 - h1
    return (True, left_hand) if left_hand != -2 else (False, score)


def finding_msg(start_repeat=1):
    i = start_repeat
    msg1 = b""
    while True:
        for j in product(range(256), repeat=i):
            msg2 = bytes(j)
            if msg1 == b"":
                msg1 = msg2
                continue
            res = check_msg(msg1, msg2)
            if res[0]:
                return (msg1, msg2) if res[1] == 1 else (msg2, msg1)
            if res[1] < 0:
                msg1 = msg2
        i += 1


print("Finding msg1 and msg2 that hash(msg1) < hash(msg2)...", end=" ", flush=True)
msg1, msg2 = finding_msg()
print("done")
print(f"msg1: {msg1}")
print(f"msg2: {msg2}")
print("result:", check_msg(msg1, msg2))

io = remote(HOST, PORT)

io.sendlineafter(b"hex): ", msg1.hex().encode())
sig1 = bytes.fromhex(io.recvline().strip().decode().split(": ")[1])
sig1_sk = [sig1[i : i + 32] for i in range(0, len(sig1), 32)]

io.sendlineafter(b"hex): ", msg2.hex().encode())
sig2 = b"".join(
    [hash(sig, h1 - h2) for sig, h1, h2 in zip(sig1_sk, hash(msg1, 1), hash(msg2, 1))]
)

io.sendlineafter(b"hex): ", sig2.hex().encode())
io.interactive()
