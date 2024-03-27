#!/usr/bin/env python3

import sys

from sage.all import *

sys.setrecursionlimit(10000)

secret = [
    (438, 3190),
    (102, 2664),
    (58, 2712),
    (229, 2954),
    (219, 3452),
    (69, 2647),
    (311, 3002),
    (303, 2647),
    (284, 2988),
    (3, 3081),
    (830, 3274),
    (-170, 2991),
    (66, 2729),
    (123, 2948),
    (99, 2967),
    (55, 2881),
    (-50, 2920),
    (169, 3152),
    (204, 2551),
    (328, 2709),
    (-99, 2753),
    (184, 2620),
    (165, 2893),
    (253, 2711),
    (298, 2443),
    (195, 3000),
    (2, 2595),
    (-164, 3003),
    (555, 2977),
    (-404, 2749),
    (146, 3079),
    (283, 2578),
]


def G(i, a, b, c):
    A = (a * 171) % 30269
    B = (b * 172) % 30307
    C = (c * 170) % 30323
    if i == 0:
        return (A + B + C) % 32
    else:
        return G(i - 1, A, B, C)


def GR(i):
    return G(i, 12643, 29806, 187)


def GI(i):
    return G(i, 3823, 25188, 24854)


def A(arr):
    res = []
    for a, b in arr:
        res.append(a)
        res.append(-b)
    return res


def B(arr):
    res = []
    for a, b in arr:
        res.append(b)
        res.append(a)
    return res


key = [[] for _ in range(32)]

for i in range(32, 0, -1):
    for j in range(32, 0, -1):
        key[i - 1].append((GR(i * 32 + j), GI(i * 32 + j)))

M = []
for k in key:
    M.append(A(k))
    M.append(B(k))

Y = []
for s in secret:
    Y.append(s[0])
    Y.append(s[1])

M = Matrix(M)
Y = vector(Y)

mapping = {}
mapping[(0, 1)] = "a"
mapping[(1, 0)] = "b"
mapping[(2, 0)] = "c"
mapping[(1, 1)] = "d"
mapping[(0, 2)] = "e"
mapping[(3, 0)] = "f"
mapping[(2, 1)] = "g"
mapping[(1, 2)] = "h"
mapping[(0, 3)] = "i"
mapping[(4, 0)] = "j"
mapping[(3, 1)] = "k"
mapping[(2, 2)] = "l"
mapping[(1, 3)] = "m"
mapping[(0, 4)] = "n"
mapping[(5, 0)] = "o"
mapping[(4, 1)] = "p"
mapping[(3, 2)] = "q"
mapping[(2, 3)] = "r"
mapping[(1, 4)] = "s"
mapping[(0, 5)] = "t"
mapping[(6, 0)] = "u"
mapping[(5, 1)] = "v"
mapping[(4, 2)] = "w"
mapping[(3, 3)] = "x"
mapping[(2, 4)] = "y"
mapping[(1, 5)] = "z"
mapping[(0, 6)] = "0"
mapping[(7, 0)] = "1"
mapping[(6, 1)] = "2"
mapping[(5, 2)] = "3"
mapping[(4, 3)] = "4"
mapping[(3, 4)] = "5"
mapping[(2, 5)] = "6"
mapping[(1, 6)] = "7"
mapping[(0, 7)] = "8"
mapping[(8, 0)] = "9"
mapping[(7, 1)] = "_"

solution = M.solve_right(Y)

flag = ""
for j in range(0, len(solution), 2):
    r = solution[j]
    i = solution[j + 1]
    flag += mapping[(r, i)]
flag = "wctf{%s}" % flag
print(flag)
