from itertools import product

from pwn import *

# nc 83.136.252.82 32328
HOST = "83.136.252.82"
PORT = 32328

io = remote(HOST, PORT)

command_ready = False


def command(cmd: bytes | str):
    global command_ready
    if isinstance(cmd, str):
        cmd = cmd.encode()

    # io.sendline(cmd)
    if command_ready:
        io.sendline(cmd)
        command_ready = False
    else:
        io.sendlineafter(b"> ", cmd)

    res = io.recvuntil(b"> ")
    if b"> " in res:
        command_ready = True
    return res


LO = 0x0
HI = 0x3

command(f"set_oe_pin({LO})")
command(f"set_ce_pin({LO})")
command(f"set_we_pin({HI})")

addr_pins = f"set_address_pins([{LO}, {LO}, {LO}, {LO}, {HI}, {HI}, {HI}, {HI}, {LO}, {LO}, {LO}])"
io_pins = f"set_io_pins([11, 12, 13, 3, 4, 5, 6, 7])"
print(addr_pins + "\n" + io_pins)
command(addr_pins)
command(io_pins)
context.log_level = "debug"
print(command(f"read_byte()"))
