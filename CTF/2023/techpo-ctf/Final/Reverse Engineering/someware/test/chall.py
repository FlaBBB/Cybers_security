import os; import py_compile
seed = os.urandom(256)
files = [file for file in os.listdir() if os.path.isfile(file)]
all_bytes = b''
enc_bytes = b''
for file in files:
    with open(file, 'rb') as f:
        all_bytes += f.read()
        
        f.close()
magic = lambda a, b: bytes.fromhex(hex(sum(list(map( lambda i: ((((a >> i) & 1) + ((b >> i) & 1)) % 2) << i, range(8)))))[2:].rjust(2, '0'))
for i in range(len(all_bytes)):
    
    enc_bytes += magic(all_bytes[i], seed[i % len(seed)])
hasil = py_compile.compile('chall.py')
f = open(hasil, 'rb').read()
template = 'import marshal\nexec(marshal.loads({}))'.format(f[16:])
with open('flag.someware', 'wb') as f:
    f.write(enc_bytes)
    f.close()
with open('chall.py', 'w') as f:
    f.write(template)
    f.close()
py_compile.compile('chall.py')
for file in files:
    os.remove(file)