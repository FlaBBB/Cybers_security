import subprocess


def execute_command_get_output(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command execution failed with error: {result.stderr}")
    return result.stdout.strip().encode()


from base64 import b64encode

from pwn import *

# nc chal.osugaming.lol 9727
HOST = "chal.osugaming.lol"
PORT = 9727

io = remote(HOST, PORT)

# solve poc
cmd = io.recvlines(2)[1]
io.sendline(execute_command_get_output(cmd))


def sign(m: bytes):
    io.sendlineafter(b"Enter your option: ", b"1")
    io.sendlineafter(b"Enter your beatmap in base64: ", b64encode(m))
    io.recvuntil(b"Okay, I've signed that for you: ")
    return io.recvline().strip()


def verify(m: bytes, s: bytes):
    io.sendlineafter(b"Enter your option: ", b"2")
    io.sendlineafter(b"Enter your beatmap in base64: ", b64encode(m))
    io.sendlineafter(b"Enter your signature for that beatmap: ", s)
    return io.recvline().strip()


dorchadas_slider = b"0,328,33297,6,0,B|48:323|61:274|61:274|45:207|45:207|63:169|103:169|103:169|249:199|249:199|215:214|205:254,1,450.000017166138,6|6,1:1|2:1,0:0:0:0:"
m = b"XIXIXI"

signature = sign(m)

cmd = f'hash_extender --data="{m.decode()}" --append="{dorchadas_slider.decode()}" --secret=244 --signature="{signature.decode()}"'
log.info(f"Executing command: {cmd}")
res = execute_command_get_output(cmd)

log.info(f"Command result: {res}")
_, _, forged_signature, forged_m = res.split(b"\n\n")[-1].split(b"\n")
forged_signature = forged_signature.split(b" ")[-1]
forged_m = bytes.fromhex(forged_m.split(b" ")[-1].decode())

log.info(f"Forged Signature: {forged_signature}")
log.info(f"Forged M: {forged_m}")

log.info(verify(forged_m, forged_signature).decode())

# io.interactive()
