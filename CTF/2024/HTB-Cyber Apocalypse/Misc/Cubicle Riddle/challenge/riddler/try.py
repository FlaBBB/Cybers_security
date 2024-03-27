import dis


def f(l):
    min = 1000
    max = -1000
    for i in l:
        if i < min:
            min = i
        if i > max:
            max = i
    return min, max


# f bytecode
bytecode = dis.Bytecode(f)
print(bytecode.dis())

bytecode = f.__code__.co_code[10:52]
print(bytecode)
dis.dis(bytecode)
# print(f.__code__.co_varnames)
# print()

# payload = b"|\x00D\x00]\x11\x00\x00}\x03|\x03|\x01k\x02\x00\x00r\x02|\x03}\x01|\x03|\x02kD\x00\x00s\x01\x8c\x10|\x03}\x02\x8c\x13\x04\x00"
# # dis.dis(payload)

# print()
# # dis.dis(b"d\x01}\x01d\x02}\x02")
# # print()
# # dis.dis(b"|\x01|\x02f\x02S\x00")
# dis.dis(b"d\x01}\x01d\x02}\x02" + payload + b"|\x01|\x02f\x02S\x00")
