# # AES 1 round 1 data attacks

# First, AES boilerplate and generate subkeys, plaintext and ciphertext.

from sage.all import *
import aes
from hashlib import md5

A = aes

key = list(md5(b"key key").digest())
expkey = A.expandKey(key, 1)
rk1 = transpose(expkey[0])
rk2 = transpose(expkey[0])
rkp = A.mixColumns(rk2[::], True)

pt = list(md5(b"plaintext").digest())

ct = list(pt)
ct = A.addRoundKey(ct[::], rk1)
ct = A.subBytes(ct[::], False)
ct = A.shiftRows(ct[::], False)

if 0: # equivalent
    ct = A.addRoundKey(ct[::], rkp)
    ct = A.mixColumns(ct[::], False)
else:
    ct = A.mixColumns(ct[::], False)
    ct = A.addRoundKey(ct[::], rk2)

print("pt", pt)
print("key", key)
print("ct", ct)
print("rk1", rk1)
print("rk2", rk2)

ctp = A.mixColumns(ct[::], True)

def backward(i):
    y = i // 4
    x = (i + y) % 4
    j = y*4 + x
    k[j] = A.rsbox[ctp[i] ^^ kp[i]] ^^ pt[j]

def forward(i):
    y = i // 4
    x = (i - y) % 4
    j = y*4 + x
    kp[j] = A.sbox[pt[i] ^^ k[i]] ^^ ctp[j]

def xor(a, b):
    return [aa ^^ bb for aa, bb in zip(a, b)]

R.<x> = GF(2)[]
F = GF(2**8, name='a', modulus=x^8+x^4+x^3+x+1)
MC = matrix(F, 4, 4, [F.fetch_int(a) for a in [2,3,1,1,  1,2,3,1,   1,1,2,3,   3,1,1,2]])

def MC_permuted(perm):
    C = copy(identity_matrix(F, 4).augment(~MC))
    C.permute_columns(Permutation([i + 1 for i in perm]))  # sage permutations indexed from 1! argh
    return copy(C.echelon_form())

def mat_mul(mat, v):
    v = [F.fetch_int(a) for a in v]
    v = mat * vector(v)
    v = [a.integer_representation() for a in v]
    return v

# Method: guess $k'_1$ and one extra byte (5 total) to work with $k_0$ and $w$.

# precompute magic matrices
M1 = MC_permuted([0, 1, 4, 7,  2, 3, 5, 6])[:,4:]

# precomputation from pt/ct
# cond 1: x + a * y = b
# cond 2: S[y] ^ t = Sinv(z ^ ctp[ci]) ^ pt[pi]
from collections import defaultdict
fa = F.fetch_int(11)
precomp = defaultdict(list)
for b in range(256):
    fb = F.fetch_int(b)
    xys = []
    for y in range(256):
        fy = F.fetch_int(y)
        fx = fb - fa * fy
        x = fx.integer_representation()
        xys.append((x, y))
    for x, y in xys:
        t = A.rsbox[x ^^ ctp[7]] ^^ pt[4] ^^ A.sbox[y]
        precomp[b,t].append((x, y))
        
print("precomp ok")

# subkey recovery progress
k = [None] * 16
kp = [None] * 16

# guesses (5 bytes)
kp[::4] = rkp[::4]
kp[3] = rkp[3]

# work out
# step 1: use single S-Boxes
backward(0)
backward(3)
backward(4)
backward(8)
backward(12)

# step 2: use K0 and w relation
k0t = A.mixColumn(kp[::4], False)

k[7] = A.rsbox[k[0] ^^ k0t[0] ^^ 1]
k[8] = A.sbox[k[15]] ^^ k0t[2]
k[12] = A.sbox[k[3]] ^^ k0t[3]
forward(7)
forward(8)
forward(12)

# step 3: guess 1 and filter 1 at the same time via precomp
fb  = F.fetch_int(9) * F.fetch_int(k[3])
fb += F.fetch_int(14) * F.fetch_int(k[7])
fb += F.fetch_int(13) * F.fetch_int(k[15])
fb += F.fetch_int(kp[6])
b = fb.integer_representation()

for x, y in precomp[b,k0t[1]]:
    print("x fixed", x, "y", y)
    k[11] = y
    k[4] = A.sbox[k[11]] ^^ k0t[1]
    kp[7] = x
    forward(4)
    forward(11)
    backward(7)
    
    delta_kp23 = A.mixColumn([k[3], k[7], k[11], k[15]], True)
    
    kp[2] = delta_kp23[0] ^^ kp[3]
    assert kp[7] == delta_kp23[1] ^^ kp[6]
    kp[11] = delta_kp23[2] ^^ kp[10]
    backward(2)
    backward(11)
    
    sol = mat_mul(M1, [kp[8]^^kp[9], kp[12]^^kp[13], k[5], k[9]])
    kp[1] = kp[0] ^^ sol[0]
    kp[5] = kp[4] ^^ sol[1]
    k[13] = sol[3]
    backward(1)
    backward(5)
    forward(13)
    if k[1] != sol[2]:  # filter
        continue
    kp[15] = delta_kp23[3] ^^ kp[14]
    backward(15) 
    break
else:
    print("failed")
    raise
    
assert k == rk1
assert kp == rkp

print("WIN!")