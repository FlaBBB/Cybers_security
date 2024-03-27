from functools import reduce

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
from sage.all import *

STATE_SIZE = 8 * 8
PASSWORD_SIZE = 32 * 4

# nc 52.59.124.14 5040
HOST = "52.59.124.14"
PORT = 5040

io = remote(HOST, PORT)


def get_next_password():
    io.sendlineafter(b">", b"1")
    io.sendlineafter(b">", b"zzz")
    io.recvuntil(b"Your password is: ")
    res = io.recvline().strip().decode()
    print(f"got pass: {res}")
    res = bytes.fromhex(res)
    return bytes_to_long(res)


n_states = []
res_state = []
rstate = []
states = []
while len(n_states) != STATE_SIZE:
    if STATE_SIZE + 1 >= len(rstate):
        s = get_next_password()
        t = []
        for _ in range(PASSWORD_SIZE):
            t.insert(0, s & 1)
            s >>= 1
        rstate += t

    n_states.append(rstate[:STATE_SIZE])

    t = "".join(map(lambda x: str(x), rstate))
    res_state.append(rstate[STATE_SIZE])
    states.append(rstate.pop(0))
    t = "".join(map(lambda x: str(x), rstate))

states += rstate
print(f"{states = }")

M = Matrix(GF(2), n_states)
V = vector(GF(2), res_state)

_TAPS = M.solve_right(V).list()
print(f"{_TAPS = }")
TAPS = []
i = 0
active = False
while len(_TAPS) > 0:
    if _TAPS.pop(0) == 1:
        TAPS.append(i)
        active = True
    if active:
        i += 1
TAPS.append(i)
print(f"{TAPS = }")


password = 0
for i in range(PASSWORD_SIZE):
    r = 0
    for t in TAPS[1:]:
        r ^= states[t - 1]
    states.insert(0, r)
    password |= states[0] << i

_password = long_to_bytes(password).hex().upper()
io.sendlineafter(b">", b"2")
io.sendlineafter(b">", _password.encode())
io.interactive()
