#!/usr/bin/env python3

import os
import secrets
import sys

from Crypto.Util.number import bytes_to_long
from PyECCArithmetic import Curve, Point


def input_int(message):
    return int(input(message), 0)


def error(message):
    print(message)
    sys.exit(0)


def main():
    flag = bytes_to_long(os.getenv("flag", "1753c{flag}").encode())

    print(
        "give me your curve, and I'll give you something to do for the next 10^20 years"
    )
    print("curve y^2=x^3+a*x+b mod p with generator g of order n")
    p = input_int("p: ")
    a = input_int("a: ") % p
    b = input_int("b: ") % p
    g = (input_int("g.x: ") % p, input_int("g.y: ") % p)
    n = input_int("n: ")

    if p < 2**256:
        error("p too small ;_;")
    if n < 2**256:
        error("n too small :[")
    if a == 0:
        error("a=0 not allowed :(")
    if b == 0:
        error("b=0 not allowed :<")

    E = Curve(a, b, p, name="big_strong_and_healthy_curve")
    g = Point(g[0], g[1], curve=E)

    if g * (n + 1) != g:
        error("you lied about the order")

    print("I'll give you the flag, if you prove that you'll be able to read it")

    challenge_priv = secrets.randbelow(n)
    challenge_pub = g * challenge_priv

    print(f"g*x: {challenge_pub.x}, {challenge_pub.y}")
    guess = input_int("what's x?: ")

    if guess != challenge_priv:
        error("this ain't it")

    print("pretty good...")
    flag_enc = g * flag
    print(f"Here's your flag: {flag_enc.x}, {flag_enc.y}")


main()
