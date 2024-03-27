import base64

def func_1(flag, unk_str):
    flag_len = len(flag)
    unk_str_len = len(unk_str)

    unk_str1 = bytearray(flag, 'utf-8')

    for i in range(flag_len):
        unk_str1[i] = unk_str1[i] ^ ord(unk_str[i % unk_str_len])

    return unk_str1.decode('utf-8')

def func_2(unk_str0):
    flag_len = len(unk_str0)
    unk_str3 = [''] * flag_len

    j = 0

    for i in range(0, flag_len , 4):
        unk_str3[j] = unk_str0[i]
        unk_str3[j + 1] = unk_str0[i + 1]
        j += 2

    for i in range(2, flag_len, 4):
        unk_str3[j] = unk_str0[i]
        unk_str3[j + 1] = unk_str0[i + 1]
        j += 2

    return ''.join(unk_str3)

def main():
    unk_str = "U2hhZG93MjAyNA=="
    unk_str = base64.b64decode(unk_str.encode('ascii')).decode('ascii')

    flag = input("Enter the input: ")

    unk_str1 = func_1(flag, unk_str)

    unk_str2 = func_2(unk_str1)

    unk_arr0 = [32, 0, 27, 30, 84, 79, 86, 22, 97, 100, 63, 95, 60, 34, 1, 71, 0, 15, 81, 68, 6, 4, 91, 40, 87, 0, 9, 59, 81, 83, 102, 21]

    for i in range(len(flag)):
        if unk_arr0[i] != ord(unk_str2[i]):
            exit(0)

    print("\nCorrect Flag!\n")

if __name__ == "__main__":
    main()
