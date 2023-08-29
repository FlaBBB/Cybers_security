from Crypto.Util.number import *
from pwn import *
from Crypto.Cipher import AES

def dec_gift(pt : bytes, key):
    iv = b"hektoday"*2
    assert len(key) == 16 and len(iv) == 16
    aes = AES.new(key.encode(), AES.MODE_CBC, iv=iv)
    return aes.decrypt(pt)

def encrypt(io, msg: bytes, IV: bytes):
    io.sendlineafter(b"[>] ", b"1")
    io.sendlineafter(b"[>] IV (hex): ", IV.hex().encode())
    io.sendlineafter(b"[>] Plaintext (hex): ", msg.hex().encode())
    return bytes.fromhex(io.recvline().split(b": ")[-1].strip().decode())[16:]

def get_gift(io):
    io.sendlineafter(b"[>] ", b"2")
    key1 = io.recvline().strip().decode()
    key2 = io.recvline().strip().decode()
    return bytes.fromhex(io.recvline().split(b": ")[-1].strip().decode()), key1, key2

# nc 103.181.183.216 18002
io = remote("103.181.183.216", 18002)

gift, key1, key2 = get_gift(io)
gift = dec_gift(gift, key2)
gift = dec_gift(gift, key1)

key1 = encrypt(io, b"\x00"*16, b"\x00"*16)[:16]
enc = encrypt(io, key1, b"\x00"*16)
key2 = encrypt(io, b"\x00"*16, enc[16:32])[:16]
flag = xor(enc[32:48], key2)
flag += gift
print(flag)