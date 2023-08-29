from pwn import *
from Crypto.Util.number import *
from tqdm import tqdm
from primefac import pollardrho_brent

def factor(N):
    res = []
    for n in tqdm(N):
        p = pollardrho_brent(n)
        res.append([p, n // p])
    return res

io = remote('103.181.183.216', 18001)
N = []
C = []
raw_temp = io.recvuntil(b"Input Full Password").decode().split("\n")
message = {}
for temp in raw_temp:
    if "Input Full Password" in temp:
        for i, n in enumerate(factor(N)):
            phi = 1
            for p in n:
                phi *= p - 1
            d = inverse(65537, phi)
            m = long_to_bytes(pow(C[i], d, N[i])).decode()
            if message.get(m) is None:
                message[m] = 1
            else:
                message[m] += 1
        message = {k: v for k, v in sorted(message.items(), key=lambda item: item[1])}
        res = []
        for m in message:
            if "happy_birthday" not in m:
                res.append(m)
    elif "n" in temp:
        N.append(int(temp.split("=")[-1]))
    elif "c" in temp:
        C.append(int(temp.split("=")[-1]))

print(res)
io.interactive()