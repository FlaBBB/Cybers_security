from pwn import *

# nc 83.136.253.226 54298
HOST = "83.136.253.226"
PORT = 54298

io = remote(HOST, PORT)
# context.log_level = "DEBUG"

payload = b"|\x00D\x00]\x12}\x03|\x03|\x01k\x00\x00\x00\x00\x00r\x02|\x03}\x01|\x03|\x02k\x04\x00\x00\x00\x00r\x02|\x03}\x02\x8c\x13"
payload = [int(b) for b in payload]
payload = b",".join([str(b).encode() for b in payload])
print(payload)

io.sendafter(b"(Choose wisely) >", b"1")
io.sendlineafter(b"(Answer wisely) >", payload)
io.interactive()
