from pwn import *
def xor(msg, key):
    o = ''
    for i in range(len(msg)):
        o += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return o

msg = ""

key = ""

print(binascii.hexlify(xor(msg, key).encode()).decode())
