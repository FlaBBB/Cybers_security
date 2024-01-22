import random

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

# nc dhash.chal.irisc.tf 10101
HOST = "dhash.chal.irisc.tf"
PORT = 10101

io = remote(HOST, PORT)


io.recvuntil(b"(")
N, e = map(int, io.recvline().strip().strip(b")").split(b", "))
d = pow(e, -1, N - 1)

payload = b""

f_block = random.randint(2, N - 2)
payload += f_block.to_bytes(256, "big")

f_block_hash = pow(f_block, e, N)
s_block_hash = random.randint(2, N - 2)
s_block = pow(s_block_hash, d, N)
payload += s_block.to_bytes(256, "big")

t_block_hash = f_block_hash ^ s_block_hash
t_block = pow(t_block_hash, d, N)
payload += t_block.to_bytes(256, "big")

io.sendlineafter(b"> ", payload.hex().encode())
io.interactive()
