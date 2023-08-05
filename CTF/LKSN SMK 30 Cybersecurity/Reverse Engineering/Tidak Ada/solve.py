import string
arr = dict()
arr[0] = 0xb3
arr[1] = 0xb4
arr[2] = 0xac
arr[3] = 0xb1
arr[4] = 0x84
arr[5] = 0x97
arr[6] = 0x9e
arr[7] = 0x93
arr[8] = 0x90
arr[9] = 0xa0
arr[10] = 0x9e
arr[11] = 0x8c
arr[12] = 0x9a
arr[13] = 0x91
arr[14] = 0x98
arr[15] = 0xa0
arr[16] = 0x9b
arr[17] = 0xde
arr[18] = 0x8c
arr[19] = 0x96
arr[20] = 0x91
arr[21] = 0xde
arr[22] = 0x82


for a in arr:
    for x in string.printable:
        x = ord(x)
        if (x&0xff|(x>>7)<<8)^0xff == arr[a]:
            print(chr(x),end='')
            break