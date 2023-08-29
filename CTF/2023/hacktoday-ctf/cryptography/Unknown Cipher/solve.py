from pwn import *
import string

def encrypt(io, msg: bytes) -> bytes:
    io.sendlineafter(b">", msg)
    temp = io.recvline().strip()
    return temp.split(b": ")[1]

# nc 103.181.183.216 19000
io = remote("103.181.183.216", 19000)

len_flag = len(encrypt(io, b""))
flag = ""

while True:
    for i in string.ascii_letters + string.digits + string.punctuation:
        c = encrypt(io, (flag + i).encode()).decode()
        ct_flag = c[-len_flag:]
        ct_input = c[:-len_flag]
        print(flag + i, end="\r")
        if ct_flag[:len(ct_input)] == ct_input:
            flag += i
            break
    assert ct_flag[:len(ct_input)] == ct_input, "something wrong!"
    if ct_flag == ct_input:
        break

print("[+] flag:", flag)