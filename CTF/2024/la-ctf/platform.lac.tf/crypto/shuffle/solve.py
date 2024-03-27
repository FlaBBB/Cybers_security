import functools
import unicodedata
from base64 import b64decode

from Crypto.Util.number import *
from pwn import *
from sympy import nextprime

DICTIONARY = ""
MESSAGE_LENGTH = 617


def gen_dictionary(length: int, begin: int = 0x0, end: int = 0x10FFFF):
    global DICTIONARY
    for i in range(begin, end):
        if (
            unicodedata.category(chr(i)) in ("Cc", "Cf", "Cs", "Co", "Cn")
            or chr(i) in DICTIONARY
        ):
            continue
        DICTIONARY += chr(i)
        if len(DICTIONARY) >= length:
            break
    DICTIONARY = (
        DICTIONARY.replace("\n", "")
        .replace("\r", "")
        .replace(" ", "")
        .replace("\t", "")
    )
    if len(DICTIONARY) < length:
        gen_dictionary(length, i, end)


class LCG:
    def __init__(self, a, c, m, seed):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        state = self.state
        self.state = (self.a * self.state + self.c) % self.m
        return state


def crt(*args):
    N = 1
    for _, n in args:
        N *= n
    result = 0
    for a, n in args:
        m = N // n
        _, inv = divmod(m, n)
        result += a * m * pow(inv, -1, n)
    return result % N, N


def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment


def crack_unknown_multiplier(states, modulus):
    multiplier = (
        (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
    )
    return crack_unknown_increment(states, modulus, multiplier)


def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(functools.reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)


# nc chall.lac.tf 31172
HOST = "chall.lac.tf"
PORT = 31172
io = remote(HOST, PORT)


def shuffle_message(msg: bytes) -> bytes:
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"?\n", msg)
    return io.recvline().strip()


def get_encrypted_secret() -> bytes:
    io.sendlineafter(b"> ", b"2")
    return io.recvline().strip().split(b": ")[1]


LIST_PRIME = []
i = nextprime(MESSAGE_LENGTH // 2)
while i < MESSAGE_LENGTH:
    LIST_PRIME.append(i)
    i = nextprime(i + 1)


def get_properties():
    enc_secret = get_encrypted_secret()

    gen_dictionary(MESSAGE_LENGTH)

    data = dict()

    N = 1
    list_prime = LIST_PRIME.copy()
    while N.bit_length() <= 65:
        i = list_prime.pop()
        r_shuffle = shuffle_message(DICTIONARY[:i].encode())
        if b"Here you go:" not in r_shuffle:
            i -= 2
            continue
        data[i] = r_shuffle.split(b": ")[1].decode()
        N *= i
        i -= 2

    states = []
    for i in range(6):
        crt_arg = []
        for k, v in data.items():
            crt_arg.append((DICTIONARY.find(v[i]), k))
        states.append(crt(*crt_arg)[0])

    return states, enc_secret


def main():
    global io
    while True:
        try:
            states, enc_secret = get_properties()

            m, a, c = crack_unknown_modulus(states)
            log.info(f"a = {a}, c = {c}, m = {m}")
            if m.bit_length() <= 58 or a.bit_length() <= 58 or c.bit_length() <= 58:
                raise ValueError(f"Invalid parameters, a = {a}, c = {c}, m = {m}")

            while m.bit_length() > 58:
                L = LCG(a, c, m, states[0])
                result = [0] * MESSAGE_LENGTH
                chosen_num = set()
                i = 0
                while result.count(0) > 0:
                    pos = L.next() % MESSAGE_LENGTH
                    if pos in chosen_num:
                        continue
                    chosen_num.add(pos)
                    result[pos] = enc_secret[i]
                    i += 1

                secret = "".join(chr(r) for r in result)
                if not secret.endswith("==."):
                    log.error(f"Invalid secret: {secret}")
                    if m % 2 == 0:
                        m // 2
                        continue
                    break
                print(b64decode(secret.encode()))
                exit(0)
        except Exception as e:
            try:
                log.error(e)
            except BaseException:
                pass
        finally:
            io.close()
            io = remote(HOST, PORT)


if __name__ == "__main__":
    main()
