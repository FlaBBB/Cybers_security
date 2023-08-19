import random
import time
import datetime  
import base64
import string

PRINTABLE = [ord(c) for c in string.printable]

def check_printable(plain):
    plain = plain
    for c in plain:
        if c not in PRINTABLE:
            return False
    return True

from Crypto.Cipher import AES

ciphertext = base64.b64decode(b"lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y")

iv = b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"

rts = 1690972020

for t in range(-12, 15):
    print(t)
    ts = rts + (t * 3600)
    for i in range(60 * 1000):
        seed = round(ts*1000) + i

        random.seed(seed)

        key = []
        for i in range(0,16):
            key.append(random.randint(0,255))

        key = bytearray(key)


        cipher = AES.new(key, AES.MODE_CBC, iv) 
        plain = cipher.decrypt(ciphertext)

        if check_printable(plain) or b"flag" in plain:
            print(plain)

# Result:
# Flag Encrypted on 2023-08-02 10:27
# lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y
