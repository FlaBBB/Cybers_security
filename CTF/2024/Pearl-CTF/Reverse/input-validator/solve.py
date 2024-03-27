import z3

key = b"oF/M5BK_U<rqxCf8zWCPC(RK,/B'v3uARD"
cipher = [
    1102,
    1067,
    1032,
    1562,
    1612,
    1257,
    1562,
    1067,
    1012,
    902,
    882,
    1397,
    1472,
    1312,
    1442,
    1582,
    1067,
    1263,
    1363,
    1413,
    1379,
    1311,
    1187,
    1285,
    1217,
    1313,
    1297,
    1431,
    1137,
    1273,
    1161,
    1339,
    1267,
    1427,
]

s = z3.Solver()

flag = [z3.BitVec(f"flag_{i}", 8) for i in range(34)]
_flag = flag.copy()

for i in range(34):
    _flag[i] ^= key[i]
    _flag[i] -= key[33 - i]

__flag = [0] * 34
for i in range(17):
    __flag[i] = _flag[1 + i * 2] * 5
    __flag[i + 17] = _flag[i * 2] * 2

for i in range(34):
    __flag[i] += 1337

for i in range(34):
    s.add(__flag[i] == cipher[i])

s.check()
m = s.model()
print("".join(chr(m[flag[i]].as_long()) for i in range(34)))
