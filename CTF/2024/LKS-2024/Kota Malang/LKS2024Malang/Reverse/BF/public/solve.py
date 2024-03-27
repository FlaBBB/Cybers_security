import string
from zlib import crc32

flag_dict = string.ascii_letters + string.digits + string.punctuation + " "

table = [
    0x0AD68E236,
    0x330C7795,
    0x2060EFC3,
    0x1AD5BE0D,
    0x0F4DBDF21,
    0x1AD5BE0D,
    0x0F3B61B38,
    0x0DA6FD2A0,
    0x0D3D99E8B,
    0x0AD68E236,
    0x0D3D99E8B,
    0x4366831A,
    0x3ABA3BBE,
    0x15D54739,
    0x4AD0CF31,
    0x6C09FF9D,
    0x0F26D6A3E,
    0x856A5AA8,
    0x6DD28E9B,
    0x76D32BE0,
    0x0F4DBDF21,
    0x6C09FF9D,
    0x6B9DF6F,
    0x6DD28E9B,
    0x29D6A3E8,
    0x0DD0216B9,
    0x84B12BAE,
    0x29D6A3E8,
    0x0A3B36A04,
    0x0F3B61B38,
    0x29D6A3E8,
    0x0F4DBDF21,
    0x4366831A,
    0x9606C2FE,
    0x0C0B506DD,
    0x29D6A3E8,
    0x270D2BDA,
    0x0F3B61B38,
    0x0FBDB2615,
    0x0FCB6E20C,
]

flag = ""
for i in range(40):
    for c in flag_dict:
        if crc32(c.encode()) & 0xFFFFFFFF == table[i]:
            flag += c
            break

print(f"{flag = }")
