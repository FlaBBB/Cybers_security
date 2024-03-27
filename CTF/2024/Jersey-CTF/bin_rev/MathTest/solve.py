import z3


def as_i64(x):
    if type(x) != int:
        x = x.as_long()
    if x < 2**63:
        return x
    return (x % 2**63) - 2**63


mult1 = z3.BitVecVal(0x9000, 64)
mult2 = z3.BitVecVal(0xDEADBEEF, 64)
mult3 = ord("O")

ans1 = z3.BitVecVal((2**63 // mult1.as_long()) + 1, 64)
ans2 = z3.BitVecVal(-1, 64)
ans3 = z3.BitVecVal(ord("o"), 8)

assert z3.simplify(mult1 * ans1).as_signed_long() < 0
assert z3.simplify(mult2 * ans2).as_signed_long() != 0
assert z3.simplify(mult3 * ans3).as_long() == ord("A")

print(ans1.as_signed_long())
print(ans2.as_signed_long())
print(chr(ans3.as_long()))

print(z3.simplify(ans1 + ans2 + z3.BitVecVal(ans3.as_long(), 64)).as_long().to_bytes(8, "little"))
