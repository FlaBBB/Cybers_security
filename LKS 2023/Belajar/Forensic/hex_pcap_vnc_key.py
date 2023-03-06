from pwn import binascii

key_down = open('key.down.txt').read().split('\n')
d = ''
for h in key_down:
    print(h[2:])
    d += binascii.unhexlify(h[2:])

print(d)