from base64 import b64encode
from pwn import *

# nc 172.86.96.174 10105
HOST = "172.86.96.174"
PORT = 10105

with open('challenge_model.h5', 'rb') as f:
    model = f.read()

io = remote(HOST, PORT)

io.sendlineafter(b"Send me your fixed model:", b64encode(model))
io.interactive()