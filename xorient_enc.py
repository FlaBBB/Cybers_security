from pwn import binascii
def xor(msg, key):
    o = ''
    for i in range(len(msg)):
        o += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return o

msg = "iki le flag e HACTFNO(yess_hoki), KEREN CUY XORIENT iki"

key = "KUNCIENG123"

print(binascii.hexlify(xor(msg, key).encode()).decode())