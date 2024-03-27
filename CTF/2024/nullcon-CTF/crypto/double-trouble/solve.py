from itertools import product

from Crypto.Cipher import AES
from Crypto.Util.number import *
from pwn import *
from tqdm import tqdm

# nc 52.59.124.14 5024
HOST = "52.59.124.14"
PORT = 5024

msg = b"A" * 28 + b"\n"

io = remote(HOST, PORT)

io.recvuntil(b"Ciphertext: 0x")
c = bytes.fromhex(io.recvline().strip().decode())

nonce = c[:12]
ct = c[12:]
log.info(f"nonce: {nonce.hex()}")
log.info(f"ct: {ct.hex()}")

io.sendafter(b"Let me encrypt one more thing for you: ", msg)

io.recvuntil(b"0x")
_key = xor(bytes.fromhex(io.recvline().strip().decode()), msg)
log.info(f"partial key: {_key.hex()}")

for k in tqdm(product(range(0x100), repeat=3), total=0x100**3):
    key = _key + bytes(k)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    _m = cipher.decrypt(ct)
    if b"ENO{" in _m:
        print(_m)
        break
