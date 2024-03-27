from pwn import *

# nc blocked1.wolvctf.io 1337
HOST = "blocked1.wolvctf.io"
# HOST = "localhost"
PORT = 1337

io = remote(HOST, PORT)


def submit_token(token: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"token > ", token)
    return io.recvline().decode().strip()


def get_token():
    io.sendlineafter(b"> ", b"2")
    return io.recvline().decode().strip()


token = get_token()
username = submit_token(token.encode()).strip("hello, ")
log.info(f"username: {username}")
log.info(f"username_len: {len(username)}")
username = username.encode()

log.info(f"token: {token}")
token_buffer = bytes.fromhex(token)
iv, data_ct = token_buffer[:16], token_buffer[16:]
log.info(f"iv: {iv.hex()}")
log.info(f"data_len: {len(data_ct)}")

target = b"doubledelete"
forged_data_ct = (
    xor(data_ct[:16], username.ljust(16, b"\x00"), target.ljust(16, b"\x00"))
    + data_ct[16:]
)
forged_token = iv.hex() + forged_data_ct.hex()
log.info(f"Forged Token: {forged_token}")
# context.log_level = "debug"
print(submit_token(forged_token.encode()))
# print(bytes.fromhex(io.recvline().decode().strip()))
# print(bytes.fromhex(io.recvline().decode().strip()))
