import functools

from Crypto.Util.number import *


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


states = [985918507, 913476731, 740056161, 2131804361, 2934336209, 3744509705]
print(crack_unknown_modulus(states))
