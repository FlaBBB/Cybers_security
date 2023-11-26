from pwn import *
import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# socket.cryptohack.org 13371
io = remote('socket.cryptohack.org', 13371)


rec = io.recvline().split(b"Alice:")[1].strip()
rec = json.loads(rec)
p = int(rec["p"], 16)
g = int(rec["g"], 16)

s = int.from_bytes(os.urandom(512), "big")
S = pow(g, s, p)

A = int(rec["A"], 16)

send = rec
send["A"] = hex(S)
send = json.dumps(send).encode()
io.sendlineafter(b"Bob:", send)

rec = io.recvline().split(b"Bob:")[1].strip()
rec = json.loads(rec)

B = int(rec["B"], 16)

send = rec
send["B"] = hex(S)
send = json.dumps(send).encode()
io.sendlineafter(b"Alice:", send)

rec = io.recvline().split(b"Alice:")[1].strip()
rec = json.loads(rec)
A_iv = bytes.fromhex(rec["iv"])
A_enc = bytes.fromhex(rec["encrypted_flag"])

K = pow(A, s, p)

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

flag = decrypt_flag(K, A_iv.hex(), A_enc.hex())
print(flag)
