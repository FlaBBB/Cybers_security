import random
from base64 import b64encode

flag = "#REDACTED#"

gen_seed = random.randint(10000, 99999)

random.seed(gen_seed)

cp = str(gen_seed % 100) + "_"

for f in flag:
    assert ord(f) <= 0xff
    temp = hex(ord(f) ^ random.randint(0, 2 ** 0xffff))[2:]
    temp = '0' * (len(temp) % 2) + temp
    cp += "".join([chr(int(temp[i:i+2], 16)) for i in range(0, len(temp), 2)])

cipher = b64encode(cp.encode('latin-1')).decode()

with open("cipher.txt", "w") as f:
    f.write("cipher: " + cipher)

