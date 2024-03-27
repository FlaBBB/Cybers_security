import ctypes
import signal
import sys

dword_70824 = 13003401
dword_70AE4 = 0
dword_70AE8 = 0
dword_70AEC = 0
byte_70B00 = [0] * 36
byte_70AC0 = 0


def check_1(a1):
    global dword_70AE4, dword_70AEC, dword_70AE8
    if a1 <= 96 or a1 > 122:
        return 0
    byte_70B00[dword_70AE4] = a1
    dword_70AE4 += 1
    if (
        (a1 == 98 or a1 == 99 or a1 == 104 or a1 == 115 or a1 == 116)
        and dword_70AEC != 2
        and dword_70AEC != 8
        and dword_70AEC != 9
        and dword_70AEC != 12
    ):
        dword_70AE8 = 1
    if a1 == 100:
        dword_70AE8 = 2
    return 1


def check_2(a1):
    global dword_70824, dword_70AE8, dword_70AEC
    if a1 <= 47 or a1 > 57:
        return 0
    if a1 - 48 != dword_70824 % 10:
        return 0
    dword_70824 //= 10
    if dword_70AEC == 3:
        dword_70AE8 = 2
    else:
        dword_70AE8 = 0
    return 1


def check_3(a1):
    global dword_70AE8
    if a1 * a1 % 9024 == 0:
        return 0
    dword_70AE8 = 0
    return 1


def protecting(function_got_protect):
    global dword_70AE8
    prot = 3
    if function_got_protect:
        prot |= 4

    if ctypes.mprotect(ctypes.addressof(check_1), ctypes.sizeof(check_1), prot) == -1:
        sys.exit("Memory protection failed")

    if function_got_protect == 1:
        prot = 3 | 4
    else:
        prot = 3

    if ctypes.mprotect(ctypes.addressof(check_2), ctypes.sizeof(check_2), prot) == -1:
        sys.exit("Memory protection failed")

    if function_got_protect == 2:
        prot = 3 | 4
    else:
        prot = 3

    if ctypes.mprotect(ctypes.addressof(check_3), ctypes.sizeof(check_3), prot) == -1:
        sys.exit("Memory protection failed")


def check_input(input):
    global dword_70AE4, dword_70AEC, dword_70AE8
    prime_sequence = []
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
    prod_input = 1

    len_input = len(input) - 1

    for v5 in range(3, 100):
        for i in range(2, v5):
            if v5 % i == 0:
                break
        else:
            prime_sequence.append(v5)

    if len_input != prime_sequence[1] * prime_sequence[2]:
        print("how?????")
        print("len_input:", len_input)
        print(
            "prime_sequence[1] * prime_sequence[2]:",
            prime_sequence[1] * prime_sequence[2],
        )
        return False

    v7 = 0
    for j in range(6):
        for k in range(6):
            if chr(input[j] ^ input[k]) != chr(v15[v7]):
                return False
            v7 += 1
        prod_input *= input[j]

    if prod_input != 1509363893664:
        print("how???")
        print("prod_input:", prod_input)
        return False

    if input[34] != 125:
        print("how?")
        print("input[34]:", input[34])
        return False

    for m in range(6, 34):
        if dword_70AE8 != -1:
            protecting(dword_70AE8)
            dword_70AE8 = -1
        if not check_1(input[m]) or not check_2(input[m]) or not check_3(input[m]):
            print("wrong in:", m)
            return False

    return "".join(byte_70B00) == "vwbowpcjrhpkobfryu"


def sub_710F9(a1, a2, a3):
    global byte_70B00, dword_70AE4
    for i in range(dword_70AE4):
        byte_70B00[i] = chr(((ord(byte_70B00[i]) - 96) % 26) + 97)
    ctypes.cast(a3 + 144, ctypes.POINTER(ctypes.c_uint))[0] = 1
    ctypes.cast(a3 + 168, ctypes.POINTER(ctypes.c_uint))[0] = ctypes.cast(
        ctypes.cast(a3 + 160, ctypes.POINTER(ctypes.POINTER(ctypes.c_uint)))[0],
        ctypes.POINTER(ctypes.c_uint),
    )[0]
    return a3


def sig_handler(signum, frame):
    pass


def main():
    signal.signal(signal.SIGSEGV, sig_handler)

    input_str = input("she r on my b till I p > ") + "\n"
    if check_input(input_str.encode()):
        print("omg how did u guess")
    else:
        print("extremely loud incorrect buzzer")


if __name__ == "__main__":
    main()
