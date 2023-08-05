from pwn import *
import subprocess
from tqdm import tqdm

RAW_MSG = "test"
TARGET_MSG = "https://www.youtube.com/@_JohnHammond"

io = connect("challenge.nahamcon.com", 32146)

io.recvuntil(b"first_part: ")

TARGET_MSG += io.recvline().strip().decode()

io.sendlineafter(b"Choice: ", b"1")
io.sendlineafter(b"msg (hex): ", binascii.hexlify(RAW_MSG.encode('latin-1')))


signature = io.recvline().strip().split(b": ")[1].decode()

info("signature: %s", signature)
info("TARGET_MSG: %s", TARGET_MSG)

is_found = False
for i in tqdm(range(10, 100 + 10 - 2)):
    hashpump_comm = "hashpump -s '" + signature + "' -d '" + RAW_MSG + "' -a '" + TARGET_MSG + "' -k " + str(i)
    
    digest, MSG = subprocess.Popen(hashpump_comm, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip().decode('unicode_escape').encode('latin-1').split(b"\n")
    
    io.sendlineafter(b"Choice: ", b"2")
    
    io.sendlineafter(b"msg (hex): ", binascii.hexlify(MSG))
    io.sendlineafter(b"tag (hex): ", digest)

    recv = io.recvline().strip()
    if recv == b"True":
        is_found = True
        break

assert is_found == True

warning("LENGTH KEY FOUND!!!")

io.sendlineafter(b"Choice: ", b"3")
io.sendlineafter(b"msg (hex): ", binascii.hexlify(MSG))
io.sendlineafter(b"tag (hex): ", digest)

# get flag
flag = io.recvline().strip().decode()
success("FLAG: %s", flag)