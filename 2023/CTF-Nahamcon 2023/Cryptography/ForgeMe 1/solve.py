import hashpumpy
from pwn import *

TARGET_MSG = "I guess you are just gonna have to include this!"
MSG = "test"

io = connect("challenge.nahamcon.com", 30002)

io.sendlineafter(b"Choice: ", b"1")
io.sendlineafter(b"msg (hex): ", binascii.hexlify(MSG.encode('latin-1')))

digest = io.recvline().strip().split(b": ")[1].decode()

digest, MSG = hashpumpy.hashpump(digest, MSG, TARGET_MSG, 64)

io.sendlineafter(b"Choice: ", b"3")
io.sendlineafter(b"msg (hex): ", binascii.hexlify(MSG.encode('latin-1')))
io.sendlineafter(b"tag (hex): ", digest.encode())

# get flag
flag = io.recvline().strip().split(b": ")[1].decode()
print(flag)