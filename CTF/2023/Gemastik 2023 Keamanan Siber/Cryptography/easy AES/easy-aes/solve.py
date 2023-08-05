from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *

HOST = "ctf-gemastik.ub.ac.id"
PORT = 10002

io = connect(HOST, PORT)

io.sendlineafter(b">", b"2")
c_secret = long_to_bytes(int(io.recvline().strip().split(b" = ")[1]))

io.sendlineafter(b">", b"1")

leaking = b"\xff"*len(c_secret)

io.sendlineafter(b"= ", str(bytes_to_long(leaking)).encode())

c_leaking = long_to_bytes(int(io.recvline().strip().split(b" = ")[1]))

key = bytearray()
for x, y in zip(leaking, c_leaking):
    key.append(x ^ y)

secret = bytearray()
for x, y in zip(key, c_secret):
    secret.append(x ^ y)

secret = bytes_to_long(secret[:128])

io.sendlineafter(b">", b"3")

io.sendlineafter(b"secret: ", str(secret).encode())

io.interactive()