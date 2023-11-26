from pwn import *
from itertools import product
from Crypto.Cipher import AES
from Crypto.Util.Padding import *

start_code = "Very simple, "

HOST = "103.145.226.206"
PORT = 1945
io = remote(HOST, PORT)

def encrypt(msg: bytes):
    io.sendlineafter(b">>", b"1")
    io.recvuntil(b"Masukan pesan: ")
    io.sendline(msg.hex())
    io.recvuntil(b"Ciphertext = ")
    return bytes.fromhex(io.recvline().strip().decode())

io.recvuntil(b"enckey = ")
enckey = io.recvline()
io.recvuntil(b"enccode = ")
# escape string decode python
enccode = eval(io.recvline().strip().decode())
io.recvuntil(b"iv2 = ")
iv2 = eval(io.recvline().strip().decode())

print(f"enckey = {enckey}")
print(f"enccode = {enccode}")
print(f"iv2 = {iv2}")

enckey = bytes.fromhex(enckey.strip().decode())
plainkey = bytearray()
for i in range(0, len(enckey)):
    plainkey.append(encrypt(plainkey + bytes([enckey[i]]))[-1])
plainkey = bytes(plainkey)[:16]

for i in product(range(0xff + 1), repeat=2):
    key = plainkey + (bytes(i) * 8)
    assert len(key) == 32
    cipher = AES.new(key, AES.MODE_CBC, iv2)
    code = (cipher.decrypt(enccode))
    # print(f"code = {code}")
    if start_code.encode("latin-1") in code:
        code = unpad(code, 16)
        print(f"key = {key}")
        print(f"code = {code}")
        break

io.sendlineafter(b">>", b"2")
io.recvuntil(b"Masukkan kode: ")
io.sendline(code)
io.interactive()