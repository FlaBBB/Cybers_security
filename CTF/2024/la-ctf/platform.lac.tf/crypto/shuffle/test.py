import math
import random
from base64 import b64encode
from secrets import randbits

from pwn import *

MESSAGE_LENGTH = 617


class LCG:

    def __init__(self, a, c, m, seed):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


def generate_random_quad():
    return randbits(64), randbits(64), randbits(64), randbits(64)


initial_iters = randbits(16)

STATES = []


def encrypt_msg(msg, params):
    global initial_iters
    a, c, m, seed = params
    L = LCG(a, c, m, seed)
    for i in range(initial_iters):
        L.next()
    l = len(msg)
    permutation = []
    chosen_nums = set()
    while len(permutation) < l:
        pos = L.next()
        if len(STATES) < 6:
            STATES.append(pos)
        pos = pos % l
        if pos not in chosen_nums:
            permutation.append(pos)
            chosen_nums.add(pos)
    output = "".join([msg[i] for i in permutation])
    return output


secret = "".join([chr(random.randint(0, 25) + ord("a")) for _ in range(MESSAGE_LENGTH)])
length = len(secret)

a, c, m, seed = params = generate_random_quad()
enc_secret = encrypt_msg(secret, params)
log.info(f"params: {a = }, {c = }, {m = }, {seed = }")
log.info(f"STATES: {STATES}")


def shuffle_message(message):
    if len(message) >= length:
        return "I ain't reading allat."
    elif math.gcd(len(message), m) != 1:
        return "Are you trying to hack me?"
    else:
        return f"Here you go: {encrypt_msg(message,params)}"


# =================================================================================================
import functools
import unicodedata
from base64 import b64decode

from Crypto.Util.number import *
from sympy import nextprime

DICTIONARY = ""


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


class LCGm:
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


LIST_PRIME = []
i = nextprime(MESSAGE_LENGTH // 2)
while i < MESSAGE_LENGTH:
    LIST_PRIME.append(i)
    i = nextprime(i + 1)


def get_properties():
    gen_dictionary(MESSAGE_LENGTH)

    data = dict()

    N = 1
    list_prime = LIST_PRIME.copy()
    while N.bit_length() <= 65:
        i = list_prime.pop()
        r_shuffle = shuffle_message(DICTIONARY[:i])
        if "Here you go:" not in r_shuffle:
            i -= 2
            continue
        data[i] = r_shuffle.split(": ")[1]
        N *= i
        i -= 2

    states = []
    for i in range(6):
        crt_arg = []
        for k, v in data.items():
            crt_arg.append((DICTIONARY.find(v[i]), k))
        states.append(crt(*crt_arg)[0])

    return states


def main():
    states = get_properties()
    log.info(f"states: {states}")
    m, a, c = crack_unknown_modulus(states)
    log.info(f"a = {a}, c = {c}, m = {m}")
    if not (m.bit_length() == 64 and a.bit_length() == 64 and c.bit_length() == 64):
        raise ValueError(f"Invalid parameters, a = {a}, c = {c}, m = {m}")

    L = LCGm(a, c, m, states[0])
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

    _secret = "".join(r for r in result)
    log.info(_secret == secret)


if __name__ == "__main__":
    main()
