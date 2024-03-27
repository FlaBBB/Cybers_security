import json

from DGA_Detection.DGA_Detection import DGADetection
from pwn import *

# nc challenges1.gcc-ctf.com 4003
HOST = "localhost"
PORT = 1337

log.info("Loading models...")
detector = DGADetection(
    "./DGA_Detection/config.json", "./DGA_Detection/model/dga_detection.v1.h5"
)
log.info("Models loaded!!!")

io = remote(HOST, PORT)

# context.log_level = "debug"
for _ in range(100):
    io.recvuntil(b"Here is a new batch of domains :")
    domains = eval(io.recvlines(2)[1].strip().decode("latin-1"))["domains"]
    log.info(f"Domains: {domains}")
    result = json.dumps({"labels": detector.predict(domains)})
    log.info(f"Result: {result}")
    io.sendlineafter(b"With 1 for dga and 0 for legit :", result.encode())

io.interactive()
