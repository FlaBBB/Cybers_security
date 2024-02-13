from pwn import *

# nc 139.162.24.230 31339
HOST = "139.162.24.230"
PORT = 31339

replacement = 0x11BE + 3
shift = 4

io = remote(HOST, PORT)

io.sendline(b"00" * 16 + b" " + str(replacement).encode() + b" " + str(shift).encode())
ciphertext = io.recvline().strip()
print(ciphertext)

io.sendline(ciphertext)
io.interactive()
