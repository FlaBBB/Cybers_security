from pwn import *

# nc 0.cloud.chals.io 30531
HOST = "0.cloud.chals.io"
PORT = 30531

io = remote(HOST, PORT)


io.sendline(b"2.3")
io.sendline(b"0.09999988079071045")
io.interactive()
