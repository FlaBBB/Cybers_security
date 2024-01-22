from z3 import *

flag = [BitVecVal(x, 8) for x in b"ON#X~o8&"]

sum = [BitVecVal(x, 8) for x in [0xCE, 0xA1, 0xAE, 0xAD, 0x64, 0x9F, 0xD5, 0]]

s = Solver()

PATH_LEN = 8
path = []
for i in range(PATH_LEN):
    path.append(BitVec(f"path[{i}]", 8))
    s.add(
        Not(Or([(path[i] & 3) == 0, path[i] % 3 == 0, path[i] > 0x64, path[i] <= 0x13]))
    )

for i in range(PATH_LEN):
    flag[i] = flag[i] ^ path[i]
    if i > 0:
        s.add(flag[i] + flag[i - 1] == sum[i - 1])

s.add(
    Or(
        [
            flag[0] == x
            for x in [
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
                71,
                73,
                79,
                83,
                89,
                97,
            ]
        ]
    )
)

if s.check() == sat:
    print("Solution found!")
    m = s.model()
    print(
        "".join([hex(m[path[i]].as_long())[2:] for i in range(PATH_LEN)][::-1])
    )  # 41565e4d2217232e

else:
    print("Can not find any solution!")
