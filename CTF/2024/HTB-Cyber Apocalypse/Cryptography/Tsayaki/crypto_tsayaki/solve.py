import os

from Crypto.Util.number import *
from pwn import *
from tea import TEA

# nc 83.136.254.223 35629
HOST = "83.136.254.223"
PORT = 35629

io = remote(HOST, PORT)

f = 1 << 31
forger1 = long_to_bytes(f | (f << 32))
forger2 = long_to_bytes((f << (32 * 2)) | (f << (32 * 3)))

iv = bytes.fromhex("0dddd2773cf4b908")
io.recvuntil(b"Here is my special message: ")
m = bytes.fromhex(io.recvline().decode().strip())
for i in range(10):
    log.info(f"Round {i + 1}")
    key = os.urandom(16)
    cipher = TEA(key, iv)
    ct = cipher.encrypt(m)
    io.sendlineafter(b"Enter your target ciphertext (in hex) : ", ct.hex().encode())
    keys = [key, xor(key, forger1), xor(key, forger2), xor(key, forger1, forger2)]
    for k in keys:
        io.sendlineafter(b"key (in hex) :", k.hex().encode())

io.interactive()
