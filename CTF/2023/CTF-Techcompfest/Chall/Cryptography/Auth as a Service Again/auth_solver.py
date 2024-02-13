import uuid, random, string, json, hashlib
import numpy as np
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
from tqdm import tqdm
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from sage.all import Matrix, Integers
from pwn import *

class Auth:
    def __init__(self):
        self.q, self.p, self.x, self.g, self.y = [0, 0, 0, 0, 0]

    def sbit(self, m: bytes) -> int:
        return sum([int(i) for i in bin(self.x ^ (bytes_to_long(m) % self.p))[2:]])

    def hash(self, m: bytes) -> int:
        return bytes_to_long(hashlib.sha256(m).digest())
    
    def verify(self, m: bytes, r: int, s: int, d: int=None) -> bool:
        sbit = self.sbit(m) if d is None else d
        def check_sig(s):
            t = pow(s, inverse(sbit, self.q - 1), self.q)
            u1 = pow(self.g, (self.hash(m) * inverse(t, self.q)) % self.q, self.p)
            u2 = pow(self.y, (r * inverse(t, self.q)) % self.q, self.p)
            return r == ((u1 * u2) % self.p) % self.q
        if (r < 2 or s < 2 or r > self.q or s > self.q): 
            return False
        if sbit % 2:
            return check_sig(s)
        else:
            sq = modular_sqrt(s, self.q)
            return any(check_sig(s) for s in [sq, (-sq) % self.q])

    def signup(self, username: str, is_admin: bool=False) -> str:
        while True:
            cookie = b64e(json.dumps({'username': username, 'is_admin': is_admin, 'uuid': str(uuid.uuid1())}).encode()).strip(b'=')
            k = random.randrange(2, self.q - 2)
            r = pow(self.g, k, self.p) % self.q
            s = pow((self.hash(cookie) + self.x * r) * inverse(k, self.q), self.sbit(cookie) ,self.q)
            if self.verify(cookie, r, s):
                return (cookie + b'.' + b64e(long_to_bytes(r)).strip(b'=') + b'.' + b64e(long_to_bytes(s)).strip(b'=')).decode()

def rstr(len):
    return ''.join(random.choice(string.ascii_letters) for _ in range(len))

def gen(m):
    p.sendlineafter(b"M> ", b"1")
    p.sendlineafter(b"username << ", m)
    p.recvuntil(b">> ")
    return p.recvline()

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

AUTH = Auth()

p = remote("ctf.ukmpcc.org", 21337)
#p = pwn.process(["python3", "auth.py"])

p.recvuntil(b"public key: ").decode()
pub = p.recvline().split(b" ")[0].decode()

AUTH.p, AUTH.g = [bytes_to_long(b64d(i+'===')) for i in pub.split('.')]
AUTH.q = (AUTH.p-1) // (AUTH.g.bit_length()-1)

assert AUTH.g <= 2**6, AUTH.g

print('P =',AUTH.p)
print('Q =',AUTH.q)
print('G =',AUTH.g)

P, Q, G = AUTH.p, AUTH.q, AUTH.g

datas = pub.encode() + b"\n"
for i in tqdm(range(1024)):
    datas += gen(rstr(i).encode())

cookies = datas[:-1].decode().split('\n')[1:]

for k in tqdm(range(245,267,2)):
    recovered_pks = []

    for n in range(len(cookies)):
        parts = cookies[n].split('.')

        M = parts[0]
        R = bytes_to_long(b64d(parts[1]+'==='))
        S = bytes_to_long(b64d(parts[2]+'==='))

        # Assume a Hamming distance
        S = pow(S, inverse(k, Q-1), Q)

        u  = inverse(S, Q)
        v  = ( AUTH.hash(M.encode()) * u ) % Q
        w  = ( R * u ) % Q
        mg = inverse(w, P-1)

        pk = pow( R * inverse( pow(G, v, P), P ), mg, P )

        recovered_pks += [pk]

    unis, cnts = np.unique(recovered_pks, return_counts=True)
    inds = [i for i in range(len(cnts)) if cnts[i] != 1]

    out = []
    if inds:
        for i in inds:
            out.append(unis[i])

out = set(out)
print(out)

for y in list(out):
    AUTH.y = y
    hamdists = []

    for k in tqdm(range(len(cookies))):
        parts = cookies[k].split('.')

        M = parts[0]
        R = bytes_to_long(b64d(parts[1]+'==='))
        S = bytes_to_long(b64d(parts[2]+'==='))

        for d in range(201,320):
            if AUTH.verify(M.encode(), R, S, d):
                hamdists += [d]
                break

    if len(hamdists) != len(cookies):
        continue

    INTS = [bytes_to_long(cookie.split('.')[0].encode()) % P for cookie in cookies]
    BITS = [[int(j) for j in list('{:0512b}'.format(i))] for i in INTS]

    DMAT = Matrix(Integers(), hamdists).T
    QMAT = Matrix(Integers(), BITS)

    print(DMAT.T)
    print(QMAT.rank())

    AUG = QMAT.augment(DMAT)
    ECH = AUG.echelon_form()

    print(ECH.row(0))
    print(ECH.column(-1))

    AUTH.x = int(''.join(['0' if i == 1 else '1' for i in ECH.column(-1).list()[:512]]),2)
    print("X =", AUTH.x)

    if AUTH.x:
        break

print('{"username": "admin", "cookie": "' + AUTH.signup("admin", True) + '"}' )
p.sendlineafter(b"M> ", b"2")
p.sendlineafter(b"<< ", b"admin")
p.sendlineafter(b"<< ", AUTH.signup("admin", True).encode())
p.interactive()