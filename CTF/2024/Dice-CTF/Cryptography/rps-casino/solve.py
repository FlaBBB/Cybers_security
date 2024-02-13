import os
import time

import z3
from Crypto.Util.number import bytes_to_long
from pwn import *

# nc mc.ax 31234
HOST, PORT = "mc.ax", 31234
io = remote(HOST, PORT)


def LFSR(state=None):
    if state is None:
        state = bytes_to_long(os.urandom(8))
    while 1:
        yield state & 0xF
        for i in range(4):
            bit = (state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1
            state = (state >> 1) | (bit << 63)


map_rps = {0: b"rock", 1: b"paper", 2: b"scissors"}


def send_choice(choice: int):
    io.sendlineafter(b"Choose rock, paper, or scissors: ", map_rps[choice])
    return io.recvline().strip()


states = []
solver = z3.Solver()

for i in range(56):
    res = send_choice(0)
    bv = z3.BitVec(f"state_{i}", 16)
    solver.add(bv >= 0, bv < 16)
    if b"win" in res:
        solver.add(bv % 3 == 2)
    elif b"lose" in res:
        solver.add(bv % 3 == 1)
    elif b"Tie" in res:
        solver.add(bv % 3 == 0)
    states.insert(0, bv)


def get(state):
    res = 0
    for i in range(4):
        res |= ((state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1) << i
        state >>= 1
    return res


for i in range(len(states)):
    if i + 16 >= len(states):
        break
    if states[i] is None:
        continue

    solver.add(get(states[i + 16] | (states[i + 15] << 4)) == states[i])


def validate(state: int):
    while state.bit_length() > 64:
        if (state >> 64) & 1 != (
            state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)
        ) & 1:
            return False
        state >>= 1
    return True


while 1:
    assert solver.check() == z3.sat, "Unsat"
    model = solver.model()
    state = 0
    for i in range(len(states)):
        state |= (model[states[i]].as_long() & 0xF) << ((len(states) - 1 - i) * 4)
    print(f"Try States: {state:x}", end=" ")
    if validate(state):
        print("correct")
        break
    solver.add(z3.Or([states[i] != model[states[i]] for i in range(16)]))
    print("incorrect")

# context.log_level = "debug"
state >>= state.bit_length() - 64
print(f"State: {state:x}")
rng = LFSR(state)
for _ in range(16):
    next(rng)
for i in range(50):
    # print(f"Round {i + 1}", end=" => ")
    print(f"Round {i + 1}")
    choice = (next(rng) + 1) % 3
    io.sendline(map_rps[choice])
io.interactive()
