from pwn import *

def attack(encrypt_oracle, unused_byte=0):
    """
    Recovers a secret which is appended to a plaintext and encrypted using ECB.
    :param encrypt_oracle: the encryption oracle
    :param unused_byte: a byte that's never used in the secret
    :return: the secret
    """
    paddings = [bytes([unused_byte] * i) for i in range(16)]
    secret = bytearray(b"")
    while True:
        padding = paddings[15 - (len(secret) % 16)]
        p = bytearray(padding + secret + b"0" + padding)
        byte_index = len(padding) + len(secret)
        end1 = len(padding) + len(secret) + 1
        end2 = end1 + len(padding) + len(secret) + 1
        for i in range(256):
            p[byte_index] = i
            c = encrypt_oracle(p)
            if c[end1 - 16:end1] == c[end2 - 16:end2]:
                secret.append(i)
                break
        else:
            secret.pop()
            break

    return bytes(secret)

def encrypt(p):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'message (in hex) = ', p.hex().encode())
    return bytes.fromhex(io.recvline()[21:].decode())

HOST = '34.101.174.85'
PORT = 10000

io = connect(HOST, PORT)

print(attack(encrypt))