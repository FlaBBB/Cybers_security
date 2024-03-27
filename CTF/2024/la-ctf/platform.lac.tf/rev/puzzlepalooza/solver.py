import z3

si128_arr = [int(x, 16) for x in "9baccb49fed06b08"]
si128_arr = [int(x, 16) for x in "6995ae4bba65f79c"] + si128_arr
si128_arr = [int(x, 16) for x in "6b4a18ed4ebcf308"] + si128_arr
si128_arr = [int(x, 16) for x in "a8d9d3e542f4dee0"] + si128_arr
si128_arr = [int(x, 16) for x in "16160e71494acf3c"] + si128_arr
si128_arr = [0xA] + si128_arr
si128 = 0
for i in range(80, -1, -1):
    si128 |= si128_arr[i] << (4 * (80 - i))
print(hex(si128))

solver = z3.Solver()

flag = [z3.BitVec(f"flag_{i}", 8) for i in range(54)]
for k in flag:
    solver.add(k >= ord("!"))
    solver.add(k < ord("~"))
for p, k in zip(b"lactf{", flag):
    solver.add(p == k)


k = 0
i = 0
while True:
    if i >= 54:
        break
    s_i = flag[i] - 64
    solver.add(s_i <= 0x3F, s_i >= 0)
    si128 ^= (s_i << (k & 7)) << ((k >> 3) * 8)  # [k >> 3]
    if (k & 7) > 2:
        si128 ^= (s_i >> (8 - (k & 7))) << (((k >> 3) + 1) * 8)  # [(k >> 3) + 1]
    k += 6
    i += 1
    if k == 324:
        solver.add(si128 & 0xF <= 8)
        for j in range(1, 81):
            solver.add((si128 >> (4 * j)) & 0xF <= 8)


if solver.check() == z3.sat:
    model = solver.model()
    flag = "".join(chr(model[f].as_long()) for f in flag)
    print(flag)
else:
    print("unsat")
