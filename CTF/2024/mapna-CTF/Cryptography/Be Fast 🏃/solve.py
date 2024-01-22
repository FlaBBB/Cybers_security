from os import urandom

from Crypto.Cipher import DES
from pwn import *

choosen_key = [
    b"00000000",
    b"00001111",
    b"01010000",
    b"01010101",
    b"10101010",
    b"11110000",
    b"11111111",
]

# nc 3.75.180.117 37773
HOST = "3.75.180.117"
PORT = 37773

io = remote(HOST, PORT)


def send_key(key):
    io.sendlineafter(b"please send your key as hex: ", key.hex().encode())


def decrypt(ct):
    for key in choosen_key:
        des = DES.new(key, DES.MODE_ECB)
        ct = des.decrypt(ct)
    ctr = 0
    while b"TOP_SECRET" not in ct:
        assert ctr < 14, "something is wrong!"
        des = DES.new(choosen_key[-1], DES.MODE_ECB)
        ct = des.decrypt(ct)
        ctr += 1

    return ct.rstrip(b"\xff")


for _ in range(7):
    send_key(urandom(8))

for key in choosen_key:
    send_key(key)

io.recvuntil(b"enc =")
enc = io.recvline().strip().decode()[2:-1]
enc = bytes.fromhex(enc)

msg = decrypt(enc)

io.sendlineafter(b"Can you guess the secret message?", msg.hex().encode())
io.interactive()
