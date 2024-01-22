from json import dumps

from pwn import *

# nc integral-communication.chal.irisc.tf 10103
HOST = "integral-communication.chal.irisc.tf"
PORT = 10103

io = remote(HOST, PORT)

org_block_0 = b'{"from": "guest"'
org_block_1 = b', "act": "echo",'

target_block_0 = b'{"from": "admin"'
target_block_1 = b', "act": "flag",'


def create_command(msg: bytes) -> (bytes, bytes):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b": ", msg)
    iv = io.recvline().strip().strip(b"IV: ").decode()
    io.recvline()
    ciphertext = io.recvline().strip().strip(b"Command: ").decode()
    return bytes.fromhex(iv), bytes.fromhex(ciphertext)


def run_command(iv: bytes, command: bytes):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b": ", iv.hex().encode())
    io.sendlineafter(b": ", command.hex().encode())
    return io.recvline().strip()


iv, ciphertext = create_command(b"aaaa")

block_ciphertext = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]

block_ciphertext[0] = xor(block_ciphertext[0], org_block_1, target_block_1)

forged_ciphertext = b"".join(block_ciphertext)

forged_plain = bytes.fromhex(
    run_command(iv, forged_ciphertext).split(b": ")[-1].decode()
)
block_forged_plain = [forged_plain[i : i + 16] for i in range(0, len(forged_plain), 16)]

forged_iv = xor(iv, block_forged_plain[0], target_block_0)

print(run_command(forged_iv, forged_ciphertext))
