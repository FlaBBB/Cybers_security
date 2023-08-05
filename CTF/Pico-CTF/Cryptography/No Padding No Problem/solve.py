from Crypto.Util.number import *
from pwn import *

conn = remote('mercury.picoctf.net', 2671)
raw_text = conn.recvuntil(b'Give me ciphertext to decrypt:').decode()

m = re.search(r"n: ([0-9]+)\ne: ([0-9]+)\nciphertext: ([0-9]+)", raw_text)
n = int(m[1])
e = int(m[2])
c = int(m[3])

to_decrypt = c * pow(2, e, n) % n

conn.sendline(str(to_decrypt).encode('latin-1'))

result = conn.recvline().decode().split(': ')[1]

m = int(result)//2

print('Result:', long_to_bytes(m))