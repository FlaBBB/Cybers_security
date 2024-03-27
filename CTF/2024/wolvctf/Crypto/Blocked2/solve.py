from pwn import *

# nc blocked2.wolvctf.io 1337
HOST = "blocked2.wolvctf.io"
PORT = 1337

io = remote(HOST, PORT)


def send_message(msg: bytes):
    io.sendlineafter(b" > ", msg.hex().encode())
    return bytes.fromhex(io.recvline().strip().decode())


io.recvuntil(b"you have one new encrypted message:")
flag_cipher = bytes.fromhex(io.recvlines(2)[1].strip().decode())
iv, flag_cipher = flag_cipher[:16], flag_cipher[16:]
flag_cipher = [flag_cipher[i : i + 16] for i in range(0, len(flag_cipher), 16)]

flag = []
last_block = iv
while len(flag) < len(flag_cipher):
    off = len(flag)
    msg = b"\x00" * 16 + last_block
    res = send_message(msg)

    _, data = res[:16], res[48:]
    assert len(data) == 16, data

    last_block = xor(data, flag_cipher[off])
    flag.append(last_block)

print(b"".join(flag).strip(b"\x00").decode())
