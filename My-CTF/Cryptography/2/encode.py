import random
from base64 import b64encode

flag = "#REDACTED#"

gen_seed = random.randint(10000, 99999)

random.seed(gen_seed)

cp = str(gen_seed % 100) + "_"

for f in flag:
    cp += chr(ord(f) ^ (random.randint(0, 2 ** 0xffff) % 0xff))

cipher = b64encode(cp.encode('latin-1')).decode()

print("cipher:", cipher)

# cipher: Njhf6/sO4vIUqtbUeBv/qgLSWphM8WVCnV3Ko+BB