import z3
from pwn import *

HOST = "94.237.59.230"
PORT = 35647

io = remote(HOST, PORT)


def get_data():
    io.recvuntil(b"You know H(")
    m = bytes.fromhex(io.recvuntil(b")")[:-1].decode().strip())
    c = bytes.fromhex(io.recvline().split(b"= ")[-1].decode().strip())
    return m, c


N = 128
_ROL_ = lambda x, i: ((x << i) | (x >> (N - i))) & (2**N - 1)
USED_STATES = []


def validate_state(state):
    if not all(0 < s < 2**N - 1 for s in state[-2:]) or not all(
        0 <= s < N for s in state[:4]
    ):
        print("Please, make sure your input satisfies the upper and lower bounds.")
        return False

    if sorted(state[:4]) in USED_STATES:
        print("You cannot reuse the same state")
        return False

    if sum(state[:4]) < 2:
        print("We have to deal with some edge cases...")
        return False

    return True


class HashRoll:
    def __init__(self):
        self.reset_state()

    def hash_step(self, i):
        r1, r2 = self.state[2 * i], self.state[2 * i + 1]
        return _ROL_(self.state[-2], r1) ^ _ROL_(self.state[-1], r2)

    def update_state(self, state=None):
        if not state:
            self.state = [0] * 6
            self.state[:4] = [random.randint(0, N) for _ in range(4)]
            self.state[-2:] = [random.randint(0, 2**N) for _ in range(2)]
        else:
            self.state = state

    def reset_state(self):
        self.update_state()

    def digest(self, buffer):
        buffer = int.from_bytes(buffer, byteorder="big")
        m1 = buffer >> N
        m2 = buffer & (2**N - 1)
        self.h = b""
        for i in range(2):
            self.h += int.to_bytes(
                self.hash_step(i) ^ (m1 if not i else m2),
                length=N // 8,
                byteorder="big",
            )
        return self.h


hashfunc = HashRoll()

solver = z3.Solver()
for i in range(3):
    solver.reset()
    m, c = get_data()
    _m = int.from_bytes(m, "big")
    _m1 = _m >> N
    _m2 = _m & (2**N - 1)
    _c = int.from_bytes(c, "big")
    _c1 = _c >> N
    _c2 = _c & (2**N - 1)

    r = [z3.BitVec(f"r{x}", N) for x in range(4)]
    solver.add(sum(r) > 2)
    for _ in r:
        solver.add(_ >= 0, _ < N)
    r0, r1, r2, r3 = r

    s = [z3.BitVec(f"s{x}", N) for x in range(2)]
    # for _ in s:
    #     solver.add(_ > 0, _ < 2**N - 1)
    s0, s1 = s

    k1 = _ROL_(s0, r0) ^ _ROL_(s1, r1)
    k2 = _ROL_(s0, r2) ^ _ROL_(s1, r3)
    solver.add(k1 ^ _m1 == _c1)
    solver.add(k2 ^ _m2 == _c2)

    for used in USED_STATES:
        asserting = []
        for j in range(4):
            asserting.append(
                z3.Not(
                    z3.And(
                        [
                            r[0] == used[0 - j],
                            r[1] == used[1 - j],
                            r[2] == used[2 - j],
                            r[3] == used[3 - j],
                        ]
                    )
                )
            )
        solver.add(z3.Or(asserting))

    assert solver.check() == z3.sat, f"model unsat in round {i + 1}"
    model = solver.model()
    state = [
        model[r0].as_long(),
        model[r1].as_long(),
        model[r2].as_long(),
        model[r3].as_long(),
        model[s0].as_long(),
        model[s1].as_long(),
    ]

    log.info(f"Round {i + 1} got state: {state}")
    log.info(f"Checking...")

    assert validate_state(state)
    hashfunc.update_state(state)
    res = hashfunc.digest(m)
    assert res == c, f"Failed, {res.hex()} != {c.hex()}"

    log.info(f"Valid")

    USED_STATES.append(sorted(state[:4]))
    io.sendlineafter(b"::", str(state).encode())

io.interactive()
