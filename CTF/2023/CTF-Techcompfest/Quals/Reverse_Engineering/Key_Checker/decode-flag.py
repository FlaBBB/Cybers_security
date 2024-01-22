from pwn import *


def from_hex_little_endian(s):
    return bytes.fromhex(s)[::-1]


s = (
    from_hex_little_endian("5a15715955270e75")
    + from_hex_little_endian("39727e370854130a")
    + from_hex_little_endian("3112464f721d1555")
    + from_hex_little_endian("5c552d5857")
)

key = xor(b"TCF2024", s, cut="min")

print(key)

flag = ""
for i in range(len(s)):
    flag += chr(s[i] ^ key[i % len(key)])
print(flag)
