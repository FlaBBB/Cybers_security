import string

import z3

flag_dict = string.ascii_letters + string.digits + "{}_"

xorerr = [
    83,
    68,
    77,
    72,
    91,
    73,
    76,
    99,
    123,
    97,
    36,
    69,
    16,
    76,
    91,
    91,
    31,
    122,
    24,
    76,
    80,
    124,
    110,
    25,
    68,
    41,
    84,
    43,
    122,
    46,
    105,
    124,
    18,
    90,
    115,
    109,
    27,
    18,
    77,
    66,
    45,
    21,
    33,
    37,
    45,
    18,
    23,
    25,
    34,
    103,
]


def apply_signal_processing(signal, c_flag, always_ten=10):
    result = 0

    if c_flag == 20:
        result = signal
    elif c_flag == 23:
        result = 8 * signal
    elif c_flag == 26:
        result = 3 * always_ten + signal
    elif c_flag == 29:
        if signal <= 1000:
            result = always_ten * always_ten * signal
        else:
            result = signal
    elif c_flag == 32:
        result = always_ten ^ signal
    elif c_flag == 35:
        if signal <= 1000000:
            if signal <= always_ten:
                result = signal
            else:
                result = signal - always_ten
        else:
            result = signal // 1000
    elif c_flag == 38:
        if signal <= always_ten:
            result = signal
        else:
            result = signal - always_ten
    elif c_flag == 41:
        if signal <= 10000:
            result = always_ten * signal
        else:
            result = signal
    elif c_flag == 44:
        result = 2 * signal
    elif c_flag == 47:
        result = signal + always_ten

    return result


def check(signals, n):
    if n == 5:
        cipher = [
            44,
            40,
            44,
            44,
            44,
            40,
            40,
            44,
            40,
            44,
            40,
            44,
            40,
            44,
            40,
            44,
            40,
            44,
            44,
            44,
            40,
            40,
            40,
            40,
            44,
            44,
            40,
            40,
            44,
            40,
            44,
            44,
            40,
            44,
            44,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
            40,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 10:
        cipher = [
            38430,
            35230,
            38430,
            38430,
            38430,
            35230,
            35230,
            38430,
            35230,
            38430,
            35230,
            38430,
            35230,
            38430,
            35230,
            38430,
            35230,
            38430,
            38430,
            38430,
            35230,
            35230,
            35230,
            35230,
            38430,
            38430,
            35230,
            35230,
            38430,
            35230,
            38430,
            38430,
            35230,
            38430,
            38430,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
            35230,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 15:
        cipher = [
            307450,
            281850,
            307450,
            307450,
            307450,
            281850,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            307450,
            307450,
            281850,
            281850,
            281850,
            281850,
            307450,
            307450,
            281850,
            281850,
            307450,
            281850,
            307450,
            307450,
            281850,
            307450,
            307450,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 20:
        cipher = [
            307470,
            281870,
            307470,
            307470,
            307470,
            281870,
            281870,
            307470,
            281870,
            307470,
            281870,
            307470,
            281870,
            307470,
            281870,
            307470,
            281870,
            307470,
            307470,
            307470,
            281870,
            281870,
            281870,
            281870,
            307470,
            307470,
            281870,
            281870,
            307470,
            281870,
            307470,
            307470,
            281870,
            307470,
            307470,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
            281870,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 25:
        cipher = [
            307450,
            281850,
            307450,
            307450,
            307450,
            281850,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            281850,
            307450,
            307450,
            307450,
            281850,
            281850,
            281850,
            281850,
            307450,
            307450,
            281850,
            281850,
            307450,
            281850,
            307450,
            307450,
            281850,
            307450,
            307450,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
            281850,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 30:
        cipher = [
            2460032,
            2255232,
            2460032,
            2460032,
            2460032,
            2255232,
            2255232,
            2460032,
            2255232,
            2460032,
            2255232,
            2460032,
            2255232,
            2460032,
            2255232,
            2460032,
            2255232,
            2460032,
            2460032,
            2460032,
            2255232,
            2255232,
            2255232,
            2255232,
            2460032,
            2460032,
            2255232,
            2255232,
            2460032,
            2255232,
            2460032,
            2460032,
            2255232,
            2460032,
            2460032,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
            2255232,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 35:
        cipher = [
            49000,
            44900,
            49000,
            49000,
            49000,
            44900,
            44900,
            49000,
            44900,
            49000,
            44900,
            49000,
            44900,
            49000,
            44900,
            49000,
            44900,
            49000,
            49000,
            49000,
            44900,
            44900,
            44900,
            44900,
            49000,
            49000,
            44900,
            44900,
            49000,
            44900,
            49000,
            49000,
            44900,
            49000,
            49000,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
            44900,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 40:
        cipher = [
            48990,
            44890,
            48990,
            48990,
            48990,
            44890,
            44890,
            48990,
            44890,
            48990,
            44890,
            48990,
            44890,
            48990,
            44890,
            48990,
            44890,
            48990,
            48990,
            48990,
            44890,
            44890,
            44890,
            44890,
            48990,
            48990,
            44890,
            44890,
            48990,
            44890,
            48990,
            48990,
            44890,
            48990,
            48990,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
            44890,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 45:
        cipher = [
            392080,
            359280,
            392080,
            392080,
            392080,
            359280,
            359280,
            392080,
            359280,
            392080,
            359280,
            392080,
            359280,
            392080,
            359280,
            392080,
            359280,
            392080,
            392080,
            392080,
            359280,
            359280,
            359280,
            359280,
            392080,
            392080,
            359280,
            359280,
            392080,
            359280,
            392080,
            392080,
            359280,
            392080,
            392080,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
            359280,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    if n == 50:
        cipher = [
            784212,
            718612,
            784212,
            784212,
            784212,
            718612,
            718612,
            784212,
            718612,
            784212,
            718612,
            784212,
            718612,
            784212,
            718612,
            784212,
            718612,
            784212,
            784212,
            784212,
            718612,
            718612,
            718612,
            718612,
            784212,
            784212,
            718612,
            718612,
            784212,
            718612,
            784212,
            784212,
            718612,
            784212,
            784212,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
            718612,
        ]
        for i in range(50):
            if cipher[i] != signals[i]:
                return False
    return True


def checker_2(flag):
    for i, x in enumerate(xorerr):
        flag[i] ^= x

    signal = [0] * 50
    signal[0] = 1
    signal[2] = 1
    signal[3] = 1
    signal[4] = 1
    signal[7] = 1
    signal[9] = 1
    signal[11] = 1
    signal[13] = 1
    signal[15] = 1
    signal[17] = 1
    signal[18] = 1
    signal[19] = 1
    signal[24] = 1
    signal[25] = 1
    signal[28] = 1
    signal[30] = 1
    signal[31] = 1
    signal[33] = 1
    signal[34] = 1
    for i in range(50):
        for j in range(50):
            signal[j] = apply_signal_processing(signal[j], flag[i], 10)
        if (i + 1) % 5 == 0:
            res = check(signal, i + 1)
            if res is False:
                return (False, i + 1)
    return (True, -1)


solver = z3.Solver()
flag = [z3.BitVec(f"flag_{i}", 8) for i in range(50)]
_flag = flag.copy()
for i in range(50):
    limiting = []
    for j, s in enumerate(flag_dict):
        limiting.append(_flag[i] == ord(s))
    solver.add(z3.Or(limiting))

known_format = "shaktictf{3l3ctr0n1cs_s0m3t1m3s_1s_p41n_7"
for i in range(len(known_format)):
    solver.add(_flag[i] == ord(known_format[i]))

for i, x in enumerate(xorerr):
    _flag[i] ^= x

solver.add((_flag[3] ^ _flag[2] ^ _flag[1] ^ _flag[0] ^ _flag[4]) == 44)
solver.add((_flag[8] ^ _flag[7] ^ _flag[6] ^ _flag[5] ^ _flag[9]) == 31)
solver.add((_flag[13] ^ _flag[12] ^ _flag[11] ^ _flag[10] ^ _flag[14]) == 29)
solver.add((_flag[18] ^ _flag[17] ^ _flag[16] ^ _flag[15] ^ _flag[19]) == 20)
solver.add((_flag[23] ^ _flag[22] ^ _flag[21] ^ _flag[20] ^ _flag[24]) == 29)
solver.add((_flag[28] ^ _flag[27] ^ _flag[26] ^ _flag[25] ^ _flag[29]) == 42)
solver.add((_flag[33] ^ _flag[32] ^ _flag[31] ^ _flag[30] ^ _flag[34]) == 31)
solver.add((_flag[38] ^ _flag[37] ^ _flag[36] ^ _flag[35] ^ _flag[39]) == 47)
solver.add((_flag[43] ^ _flag[42] ^ _flag[41] ^ _flag[40] ^ _flag[44]) == 43)
solver.add((_flag[48] ^ _flag[47] ^ _flag[46] ^ _flag[45] ^ _flag[49]) == 42)
solver.add(_flag[0] == 32)
solver.add(_flag[5] == 32)
solver.add(_flag[10] == 23)
solver.add(_flag[15] == 41)
solver.add(_flag[20] == 35)
solver.add(_flag[25] == 26)
solver.add(_flag[30] == 26)
solver.add(_flag[35] == 29)
solver.add(_flag[40] == 26)
solver.add(_flag[45] == 38)
solver.add(_flag[4] == 47)
solver.add(_flag[9] == 26)
solver.add(_flag[14] == 47)
solver.add(_flag[19] == 47)
solver.add(_flag[24] == 41)
solver.add(_flag[29] == 29)
solver.add(_flag[34] == 44)
solver.add(_flag[39] == 29)
solver.add(_flag[44] == 20)
solver.add(_flag[49] == 26)

corret_offset = 0
saved_flag = ""
while solver.check() == z3.sat:
    model = solver.model()
    r_flag = [model[flag[i]].as_long() for i in range(50)]
    s_flag = "".join(map(chr, r_flag))
    is_correct, w_offset = checker_2(r_flag)
    if is_correct:
        print(f"\nflag: {s_flag}")
        break
    print(
        f"                           \rWrong at {w_offset} with flag: " + s_flag,
        end="",
    )
    if corret_offset != w_offset:
        print(
            f"                                                     \rCorrecting from {corret_offset} to {w_offset} with flag: "
            + s_flag
        )
        for i in range(corret_offset, w_offset - 5):
            solver.add(_flag[i] == r_flag[i])
        corret_offset = w_offset
        saved_flag = s_flag
    re_add = []
    for i in range(w_offset - 5, w_offset):
        re_add.append(_flag[i] != r_flag[i])
    solver.add(z3.Or(re_add))
