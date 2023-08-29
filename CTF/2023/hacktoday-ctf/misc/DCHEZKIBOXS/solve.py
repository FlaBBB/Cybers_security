from pwn import *

# context.log_level = "debug"
DICT = "BCDEHIKOX"

# nc 103.181.183.216 19001
io = remote("103.181.183.216", 19001)

question = io.recvline().decode().strip()

# type 1
# answer = ""
# temp = ""
# for i in question:
#     if i in DICT:
#         temp += i
#     else:
#         if len(temp) > len(answer):
#             answer = temp
#         temp = ""

# type 2
answer = ""
for i in question:
    if i in DICT:
        answer += i
    

print(answer)

io.sendlineafter(b"password:", answer.encode())

io.interactive()