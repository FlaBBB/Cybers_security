import z3

solver = z3.Solver()

flag = [z3.BitVec(f"flag_{i}", 8) for i in range(36)]

_flag = flag.copy()

for i in range(36):
    if i % 2 == 0:
        _flag[i] ^= 0x38

for i in range(36):
    _flag[i] -= 5

for i in range(6):
    _flag[i], _flag[i + 18] = _flag[i + 18], _flag[i]

for i in range(6):
    _flag[6 * i + 1], _flag[6 * i + 4] = _flag[6 * i + 4], _flag[6 * i + 1]

for i in range(6):
    _flag[i + 6], _flag[i + 30] = _flag[i + 30], _flag[i + 6]

for i in range(6):
    _flag[6 * i + 2], _flag[6 * i + 3] = _flag[6 * i + 3], _flag[6 * i + 2]

solver.add(_flag[6] + _flag[16] - _flag[18] == 106)
solver.add(_flag[10] + _flag[32] - _flag[29] == 174)
solver.add(_flag[34] + _flag[2] - _flag[17] == 111)
solver.add(_flag[14] + _flag[18] - _flag[28] == 19)
solver.add(_flag[23] + _flag[9] - _flag[2] == 16)
solver.add(_flag[1] + _flag[21] - _flag[27] == 75)
solver.add(_flag[26] + _flag[5] - _flag[6] == 111)
solver.add(_flag[20] + _flag[13] - _flag[33] == 83)
solver.add(_flag[27] + _flag[8] - _flag[26] == 113)
solver.add(_flag[2] + _flag[20] - _flag[5] == 89)
solver.add(_flag[17] + _flag[26] - _flag[35] == 141)
solver.add(_flag[5] + _flag[6] - _flag[15] == 115)
solver.add(_flag[29] + _flag[14] - _flag[31] == 18)
solver.add(_flag[25] + _flag[30] - _flag[3] == 155)
solver.add(_flag[21] + _flag[0] - _flag[19] == 84)
solver.add(_flag[7] + _flag[22] - _flag[13] == 31)
solver.add(_flag[15] + _flag[11] - _flag[24] == 187)
solver.add(_flag[3] + _flag[27] - _flag[7] == 102)
solver.add(_flag[13] + _flag[4] - _flag[32] == 51)
solver.add(_flag[28] + _flag[17] - _flag[14] == 141)
solver.add(_flag[19] + _flag[10] - _flag[0] == 102)
solver.add(_flag[22] + _flag[35] - _flag[20] == 40)
solver.add(_flag[24] + _flag[1] - _flag[12] == 22)
solver.add(_flag[11] + _flag[28] - _flag[8] == 109)
solver.add(_flag[18] + _flag[23] - _flag[25] == 95)
solver.add(_flag[34] + _flag[0] + _flag[7] == 184)
solver.add(_flag[12] + _flag[25] - _flag[1] == 60)
solver.add(_flag[8] + _flag[19] - _flag[21] == 96)
solver.add(_flag[30] + _flag[33] - _flag[10] == 73)
solver.add(_flag[30] + _flag[35] + _flag[3] == 135)
solver.add(_flag[16] + _flag[29] - _flag[9] == 130)
solver.add(_flag[22] + _flag[9] + _flag[15] == 179)
solver.add(_flag[31] + _flag[34] - _flag[4] == 87)
solver.add(_flag[4] + _flag[12] - _flag[16] == 83)
solver.add(_flag[33] + _flag[31] - _flag[23] == 64)
solver.add(_flag[5] + _flag[4] + _flag[3] + _flag[2] + _flag[1] + _flag[0] == 458)
solver.add(_flag[11] + _flag[10] + _flag[9] + _flag[8] + _flag[7] + _flag[6] == 425)
solver.add(_flag[17] + _flag[16] + _flag[15] + _flag[14] + _flag[13] + _flag[12] == 445)
solver.add(_flag[23] + _flag[22] + _flag[21] + _flag[20] + _flag[19] + _flag[18] == 526)
solver.add(_flag[29] + _flag[28] + _flag[27] + _flag[26] + _flag[25] + _flag[24] == 418)
solver.add(_flag[35] + _flag[34] + _flag[33] + _flag[32] + _flag[31] + _flag[30] == 522)
solver.add(_flag[30] + _flag[24] + _flag[18] + _flag[12] + _flag[6] + _flag[0] == 394)
solver.add(_flag[31] + _flag[25] + _flag[19] + _flag[13] + _flag[7] + _flag[1] == 382)
solver.add(_flag[32] + _flag[26] + _flag[20] + _flag[14] + _flag[8] + _flag[2] == 560)
solver.add(_flag[33] + _flag[27] + _flag[21] + _flag[15] + _flag[9] + _flag[3] == 357)
solver.add(_flag[34] + _flag[28] + _flag[22] + _flag[16] + _flag[10] + _flag[4] == 599)
solver.add(_flag[35] + _flag[29] + _flag[23] + _flag[17] + _flag[11] + _flag[5] == 502)

solver.check()
model = solver.model()
r_flag = [model[flag[i]].as_long() for i in range(36)]
print(bytes(r_flag).decode())
