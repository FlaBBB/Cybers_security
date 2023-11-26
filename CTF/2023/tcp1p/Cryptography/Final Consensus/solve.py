from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from tqdm import tqdm

# nc ctf.tcp1p.com 35257
HOST = "ctf.tcp1p.com"
PORT = 35257

io = remote(HOST, PORT)


E_FLAG = io.recvline().strip().strip(b"Alice: My message ").decode()
# print(E_FLAG)
E_FLAG = bytes.fromhex(E_FLAG)

send_message = b"qwertyuiop"

io.sendlineafter(b">> ", send_message);
io.recvuntil(b"Steve: ")

known_message = pad(send_message, 16)
known_ct = bytes.fromhex(io.recvline().strip().decode())

encryption_table = {}
for key in tqdm(range(1000000)):
    key = (str(key).zfill(6)*4)[:16].encode()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    ct = cipher.encrypt(known_message)
    encryption_table[ct] = key

decryption_table = {}
for key in tqdm(range(1000000)):
    key = (str(key).zfill(6)*4)[:16].encode()
    cipher = AES.new(key, mode=AES.MODE_ECB)
    ct = cipher.decrypt(known_ct)
    decryption_table[ct] = key

encryption_table_set = set(encryption_table.keys())
decryption_table_set = set(decryption_table.keys())

intersection = encryption_table_set.intersection(decryption_table_set).pop()
encryption_key = encryption_table[intersection]  
decryption_key = decryption_table[intersection]  

# now decrypt flag_enc twice
cipher1 = AES.new(encryption_key, AES.MODE_ECB)
cipher2 = AES.new(decryption_key, AES.MODE_ECB)

FLAG = cipher2.decrypt(E_FLAG)
FLAG = cipher1.decrypt(FLAG).decode().strip()

print(FLAG)