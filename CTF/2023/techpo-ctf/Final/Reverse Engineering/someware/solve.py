def encrypt(d):
    import os
    import py_compile

    seed = os.urandom(256)
    files = [f for f in os.listdir() if os.path.isfile(f)]
    all_bytes = b''
    enc_bytes = b''

    for file in files:
        with open(file, 'rb') as f:
            all_bytes += f.read()
            f.close()

    def just_adding(a, b):
        return hex((a + b))[2:].rjust(2, '0')

    for i in range(len(all_bytes)):
        enc_bytes += just_adding(all_bytes[i], seed[i % len(seed)])

    hasil = py_compile.compile('chall.py')

    with open(hasil, 'rb') as f:
        template = 'import marshal\nexec(marshal.loads({}))'.format(f.read()[16:])

    with open('flag.someware', 'wb') as f:
        f.write(enc_bytes)
        f.close()

    with open('chall.py', 'w') as f:
        f.write(template)
        f.close()

    py_compile.compile('chall.py')

    for file in files:
        os.remove(file)

def just_minus(c, a):
    return c - a

with open("flag.someware", "rb") as f:
    cipher = f.read()
    f.close()

with open("chall-dec.py", "rb") as f:
    knowed_file = f.read()[:256]
    f.close()

print(len(cipher))
print(len(knowed_file))

known_message = b"import os; import py_compile\nseed = os.urandom(256)\nfiles = [file for file in os.listdir() if os.path.isfile(file)]"

from pwn import xor
from tqdm import tqdm

# print(f"{partialkey = }")
for i in tqdm(range(0, len(cipher))):
    partialkey = xor(known_message, cipher[i:i+len(known_message)])
    for j in range(0, len(cipher)):
        temp = xor(cipher[j:j+len(known_message)], partialkey)
        if b"flag{" in temp:
            print(temp)