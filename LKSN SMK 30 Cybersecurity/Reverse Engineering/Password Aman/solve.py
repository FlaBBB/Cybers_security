def stuff_funct(chr):
    res = ord(chr) ^ 0xffffffff
    for _ in list(range(8))[::-1]:
        res = -(res & 1) & 0xedb88320 ^ (res >> 1)
    return ~res & 0xffffffff

arr = dict()
arr[0] = 0xad68e236
arr[1] = 0x330c7795
arr[2] = 0x2060efc3
arr[3] = 0x4366831a
arr[4] = 0x15d54739
arr[5] = 0x916b06e7
arr[6] = 0xf3b61b38
arr[7] = 0x1b0ecf0b
arr[8] = 0x916b06e7
arr[9] = 0x29d6a3e8
arr[10] = 0x3dd7ffa7
arr[11] = 0x5767df55
arr[12] = 0x3dd7ffa7
arr[13] = 0x6dd28e9b
arr[14] = 0x1ad5be0d
arr[15] = 0xfcb6e20c

import string
for a in arr:
    for b in string.printable:
        if stuff_funct(b) == arr[a]:
            print(b, end='')
            break