ARR1 = [11113, 12554, 5608, 11108, 5724, 5724, 6128, 11403, 5273, 9654, 5299, 5583, 5829, 9353, 12679, 12289, 11118, 13422, 5218, 11301, 11068, 10909, 12795, 11108, 5758]
ARR2 = [191, 125, 61, 68, 69, 36, 99, 119, 77, 126, 101, 56, 44, 28, 146, 115, 119, 82, 47, 161, 161, 125, 165, 139, 103]
VAR3 = [0x0E3,0x0DF,0x92,0x0CF,0x0EF,0x0D6,0x66,0x0E2,0x0D8,0x8F,0x0E7,0x0C7,0x61,0x0E7,0x0BE,0x64,0x0D6,0x0D1,0x0A6,0x99,0x0A5,0x0ED,0x0D4,0x0DE,0x92,0x0CD,0x0AD,0x0D2,0x0DB,0x0D6,0x93,0x0DB,0x0CD,0x0A7,0x93,0x0BE,0x0EE,0x60,0x0EE,0x0BE,0x93,0x0A7,0x0CD,0x0DB,0x93,0x0D6,0x0DB,0x0D2,0x0AD,0x0CD,0x92,0x0DE,0x0D4,0x0ED,0x0A5,0x99,0x0A6,0x0D1,0x0D6,0x64,0x0BE,0x0E7,0x61,0x0C7,0x0E7,0x8F,0x0D8,0x0E2,0x66,0x0D6,0x0EF,0x0CF,0x92,0x0DF,0x0E3]

def validator(flag:bytes):
    assert len(flag) == 75
    i = 0
    j = 0
    while i <= 24 :
        assert not (j < 75 and (flag[j+1] * flag[j]) ^ flag[j+2] != ARR1[i])
        j += 3
        i += 1
    for i in range(75):
        assert not (flag[i] + flag[74 - i] != VAR3[i])
    for j in range(38):
        flag[j], flag[74 - j] = flag[74 - j], flag[j]
    i = 0
    j = 0
    while i <= 24:
        assert not (j < 75 and flag[j+1] + flag[j] - flag[j + 2] != ARR2[i])
        j += 3
        i += 1

import z3

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(75)]
s = z3.Solver()
for f in flag:
    s.add(f >= 0x20, f <= 0x7e)

i = 0
j = 0
while i <= 24 :
    # assert not (j < 75 and (flag[j+1] * flag[j]) ^ flag[j+2] != ARR1[i])
    s.add((flag[j+1] * flag[j]) ^ flag[j+2] == ARR1[i])
    j += 3
    i += 1
for i in range(75):
    # assert not (flag[i] + flag[74 - i] != VAR3[i])
    s.add(flag[i] + flag[74 - i] == VAR3[i])
for j in range(38):
    flag[j], flag[74 - j] = flag[74 - j], flag[j]
i = 0
j = 0
while i <= 24:
    # assert not (j < 75 and flag[j+1] + flag[j] - flag[j + 2] != ARR2[i])
    s.add(flag[j+1] + flag[j] - flag[j + 2] == ARR2[i])
    j += 3
    i += 1

print(s.check())
model = s.model()
res = bytearray(75)
for m in model:
    res[int(m.name()[5:])] = model[m].as_long()
print(res)