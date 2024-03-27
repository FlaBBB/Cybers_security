import z3

v15 = [
    0,
    0xD,
    0xF,
    0x18,
    0xA,
    0x17,
    0xD,
    0,
    2,
    0x15,
    7,
    26,
    15,
    2,
    0,
    23,
    5,
    24,
    24,
    21,
    23,
    0,
    18,
    15,
    10,
    7,
    5,
    18,
    0,
    29,
    23,
    26,
    24,
    15,
    29,
    0,
]


def shift(gathered):
    for i in range(len(gathered)):
        gathered[i] = (gathered[i] - 96) % 26 + 97


def go_to(m, idx, x, n, gathered, f_id):
    if f_id == 0:
        return check_1(m, idx, x, n, gathered, f_id)
    if f_id == 1:
        shift(gathered)
        return check_2(m, idx, x, n, gathered, f_id)
    if f_id == 2:
        shift(gathered)
        shift(gathered)
        return check_3(m, idx, x, n, gathered, f_id)


def check_1(m, idx, x, n, gathered, f_id):
    # print(f"access function check_1 with {m[idx]}, {x}")
    if idx == 34:
        return (True, idx, "done")
    if m[idx] <= 96 or m[idx] > 122:
        return (False, idx, "invalid char in check_1")
    gathered.append(m[idx])
    if m[idx] == 98 or m[idx] == 99 or m[idx] == 104 or m[idx] == 115 or m[idx] == 116:
        x += 1
        if x != 2 and x != 8 and x != 9 and x != 12:
            f_id = 1

    if m[idx] == 100:
        f_id = 2

    shift(gathered)
    shift(gathered)
    return go_to(m, idx + 1, x, n, gathered, f_id)


def check_2(m, idx, x, n, gathered, f_id):
    # print(f"access function check_2 with {m[idx]}, {x}")
    if idx == 34:
        return (True, idx, "done")
    if m[idx] <= 47 or m[idx] > 57:
        return (False, idx, "invalid char in check_2")
    if m[idx] - 48 != n % 10:
        return (False, idx, "invalid digit in check_2")
    n //= 10

    if x == 3:
        f_id = 2
    else:
        f_id = 0
    shift(gathered)
    return go_to(m, idx + 1, x, n, gathered, f_id)


def check_3(m, idx, x, n, gathered, f_id):
    # print(f"access function check_3 with {m[idx]}, {x}")
    if idx == 34:
        return (True, idx, "done")
    if m[idx] * m[idx] % 9024 == 0:
        return (False, idx, "invalid char in check_3")
    return go_to(m, idx + 1, x, n, gathered, 0)


def checker(m):
    idx = 6
    x = 0
    n = 13003401
    f_id = 0
    gathered = []
    res = check_1(m, idx, x, n, gathered, f_id)
    if not res[0]:
        return res
    return ("".join(chr(x) for x in gathered) == "vwbowpcjrhpkobfryu", res[1], "done")


solver = z3.Solver()

input = [z3.BitVec(f"input_{i}", 16) for i in range(36)]
for i in range(35):
    solver.add(48 <= input[i], input[i] <= 125)
solver.add(input[-1] == ord("\n"))

prod_input = 1
for i in range(6):
    for j in range(6):
        solver.add(input[i] ^ input[j] == v15[i * 6 + j])
    prod_input *= input[i]

solver.add(prod_input == 1509363893664)
solver.add(input[34] == 125)

const = 0
# m[idx] == 98 or m[idx] == 99 or m[idx] == 104 or m[idx] == 115 or m[idx] == 116
for i in range(6, 34):
    solver.add(
        z3.Or(
            z3.And(input[i] > 47, input[i] <= 57),
            z3.And(input[i] > 96, input[i] <= 122),
        )
    )
    const += input[i] / 96
    if i != 6:
        solver.add(
            z3.If(
                z3.Or(
                    input[i - 1] == 98,
                    input[i - 1] == 99,
                    input[i - 1] == 104,
                    input[i - 1] == 115,
                    input[i - 1] == 116,
                ),
                z3.Or([input[i] - 48 == j for j in set([1, 3, 0, 0, 3, 4, 0, 1])]),
                z3.If(
                    input[i - 1] != 100, z3.And(input[i] > 96, input[i] <= 122), True
                ),
            )
        )

solver.add(const == 18)

while solver.check() == z3.sat:
    model = solver.model()
    flag = "".join(chr(model[input[i]].as_long()) for i in range(36))
    check = checker(flag.encode())
    if not check[0]:
        recheck = []
        for i in range(check[1] + 1):
            recheck.append(input[i] != model[input[i]])
        solver.add(z3.Or(recheck))
        print(
            f"invalid char at {check[1]}, with input = {flag[:-1]}                                ",
            end="\r",
        )
        continue
    print(flag)
    exit(0)
print("unsat")
