from pwn import *

# nc tagseries1.wolvctf.io 1337
HOST = "tagseries1.wolvctf.io"
PORT = 1337

io = remote(HOST, PORT)
io.recvline()


def send_message(message, tag):
    io.sendline(message)
    io.sendline(tag)
    return io.recvline().strip()


def padding(msg, padded_by, size=16):
    return msg + (padded_by * (size - len(msg) % size))


MESSAGE = b"GET FILE: flag.txt"

msg1 = padding(MESSAGE, b"A") + b"A" * 16
tag = send_message(msg1, b"A" * 16)

msg2 = padding(MESSAGE, b"B") + b"A" * 16
print(send_message(msg2, tag))
