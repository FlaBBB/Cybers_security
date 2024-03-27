from pwn import *

# nc tagseries2.wolvctf.io 1337
HOST = "tagseries2.wolvctf.io"
# HOST = "localhost"
PORT = 1337

io = remote(HOST, PORT)
io.recvline()


def send_message(message, tag):
    io.sendline(message)
    io.sendline(tag)
    # io.recvline()
    return io.recvline().strip()


def padding(msg, padded_by, size=16):
    return msg + (padded_by * (size - len(msg) % size))


MESSAGE = b"GET: flag.txt"

# context.log_level = "debug"
# Round 1
msg = padding(MESSAGE, b"A")
r0 = send_message(msg, b"A" * 16)

# Round 2
msg = padding(MESSAGE, b"A") + (16).to_bytes(16, "big") + b"A" * 16
r1 = send_message(msg, b"A" * 16)

# Round 3
msg = (
    padding(MESSAGE, b"A")
    + (16).to_bytes(16, "big")
    + b"A" * 16
    + (16 * 3).to_bytes(16, "big")
    + b"B" * 16
)
tag = send_message(msg, b"A" * 16)

msg = (
    padding(MESSAGE, b"A")
    + (16).to_bytes(16, "big")
    + xor(b"B" * 16, r0, r1)
    + (16 * 5).to_bytes(16, "big")
    + xor(b"B" * 16, tag, r1)
)
print(send_message(msg, tag))
