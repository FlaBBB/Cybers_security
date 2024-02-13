# .data:0000000000004060 flag            db 0Ch, 5Ch, 60h, 20h, 69h, 63h, 64h, 0Fh, 4Fh, 1Eh, 33h
# .data:0000000000004060                                         ; DATA XREF: check+5F↑o
# .data:000000000000406B                 db 3Ah, 68h, 2Ah, 7Ch, 0D9h, 0D5h, 0D0h, 0C9h, 0E7h, 0C3h
# .data:0000000000004075                 db 0F0h, 0BCh, 0ABh, 9Bh, 0D7h, 98h, 8Bh, 0AFh, 0B0h, 0F8h
# .data:000000000000407F                 db 47h, 49h, 16h, 49h, 68h, 1Ch dup(0)

# .data:00000000000040A0 KEY             db 7Bh, 3Dh, 14h, 43h, 1, 43h, 5Eh, 2Fh, 27h, 6Ah, 47h
# .data:00000000000040A0                                         ; DATA XREF: check+40↑o
# .data:00000000000040AB                 db 4Ah, 1Bh, 10h, 53h, 0F6h, 0ACh, 0BFh, 0BCh, 93h, 0B6h
# .data:00000000000040B5                 db 2 dup(0DEh), 0CEh, 0B4h, 0B3h, 0C9h, 0FCh, 9Bh, 0C7h
# .data:00000000000040BE                 db 0C1h, 10h, 2Eh, 4Eh, 2Ah, 39h

flag = [
    0x0C,
    0x5C,
    0x60,
    0x20,
    0x69,
    0x63,
    0x64,
    0x0F,
    0x4F,
    0x1E,
    0x33,
    0x3A,
    0x68,
    0x2A,
    0x7C,
    0xD9,
    0xD5,
    0xD0,
    0xC9,
    0xE7,
    0xC3,
    0xF0,
    0xBC,
    0xAB,
    0x9B,
    0xD7,
    0x98,
    0x8B,
    0xAF,
    0xB0,
    0xF8,
    0x47,
    0x49,
    0x16,
    0x49,
    0x68,
    0x1C,
    0,
]
key = [
    0x7B,
    0x3D,
    0x14,
    0x43,
    0x01,
    0x43,
    0x5E,
    0x2F,
    0x27,
    0x6A,
    0x47,
    0x4A,
    0x1B,
    0x10,
    0x53,
    0xF6,
    0xAC,
    0xBF,
    0xBC,
    0x93,
    0xB6,
    0xDE,
    0xDE,
    0xCE,
    0xB4,
    0xB3,
    0xC9,
    0xFC,
    0x9B,
    0xC7,
    0xC1,
    0x10,
    0x2E,
    0x4E,
    0x2A,
    0x39,
]

FLAG = ""
for i in range(36):
    FLAG += chr(flag[i] ^ key[i])

print(FLAG)
print(ord("w"))