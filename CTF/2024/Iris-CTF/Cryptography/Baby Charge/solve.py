from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

# nc babycha.chal.irisc.tf 10100
HOST = "babycha.chal.irisc.tf"
PORT = 10100

io = remote(HOST, PORT)


def ROTL(a, b):
    return (((a) << (b)) | ((a % 2**32) >> (32 - (b)))) % 2**32


def qr(x, a, b, c, d):
    x[a] += x[b]
    x[d] ^= x[a]
    x[d] = ROTL(x[d], 16)
    x[c] += x[d]
    x[b] ^= x[c]
    x[b] = ROTL(x[b], 12)
    x[a] += x[b]
    x[d] ^= x[a]
    x[d] = ROTL(x[d], 8)
    x[c] += x[d]
    x[b] ^= x[c]
    x[b] = ROTL(x[b], 7)


ROUNDS = 20


def chacha_block(inp):
    x = list(inp)
    for i in range(0, ROUNDS, 2):
        qr(x, 0, 4, 8, 12)
        qr(x, 1, 5, 9, 13)
        qr(x, 2, 6, 10, 14)
        qr(x, 3, 7, 11, 15)

        qr(x, 0, 5, 10, 15)
        qr(x, 1, 6, 11, 12)
        qr(x, 2, 7, 8, 13)
        qr(x, 3, 4, 9, 14)

    return [(a + b) % 2**32 for a, b in zip(x, inp)]


def gen_buffer_from_state(state):
    return b"".join(long_to_bytes(x).rjust(4, b"\x00") for x in state)


def encrypt_input(input: bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"? ", input)
    return bytes.fromhex(io.recvline().strip().decode())


def encrypt_flag():
    io.sendlineafter(b"> ", b"2")
    return bytes.fromhex(io.recvline().strip().decode())


def get_current_state():
    inp = b"a" * (16 * 4)
    c = encrypt_input(inp)
    state = []
    for i in range(0, len(c), 4):
        state.append(bytes_to_long(xor(c[i : i + 4], b"aaaa")))
    return state


state = get_current_state()
new_state = chacha_block(state)
buffer = gen_buffer_from_state(new_state)

enc_flag = encrypt_flag()
flag = xor(enc_flag, buffer[: len(enc_flag)])
print(flag)
