import string
from base64 import b64decode

from pwn import *

flag_dict = string.ascii_letters + string.digits + "{}_"

# nc dyn.ctf.pearlctf.in 30015
HOST = "dyn.ctf.pearlctf.in"
PORT = 30015

io = remote(HOST, PORT)


def attack(encrypt_oracle, dictionary: bytes = None, unused_byte=0):
    """
    Recovers a secret which is appended to a plaintext and encrypted using ECB.
    :param encrypt_oracle: the encryption oracle
    :param unused_byte: a byte that's never used in the secret
    :return: the secret
    """
    paddings = [bytes([unused_byte] * i) for i in range(32)]
    secret = bytearray("")
    while True:
        padding = paddings[31 - (len(secret) % 32)]
        p = bytearray(padding + secret + b"0" + padding)
        byte_index = len(padding) + len(secret)
        end1 = len(padding) + len(secret) + 1
        end2 = end1 + len(padding) + len(secret) + 1
        for i in range(256) if dictionary is None else dictionary:
            p[byte_index] = i
            c = encrypt_oracle(p)
            if c[end1 - 16 : end1] == c[end2 - 16 : end2]:
                secret.append(i)
                break
        else:
            secret.pop()
            break

    return bytes(secret)


def encrypt(data: bytes):
    global io
    io.sendlineafter(b"Enter plaintext: ", data)
    res = io.recvline().strip()
    return b64decode(res)


flag = attack(encrypt, dictionary=flag_dict.encode(), unused_byte=ord("`"))
print(flag)
