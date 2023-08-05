from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import functools

class LCG:
    def __init__(self, lcg_s, lcg_m, lcg_c, lcg_n):
        self.state = lcg_s
        self.lcg_m = lcg_m
        self.lcg_c = lcg_c
        self.lcg_n = lcg_n

    def next(self):
        self.state = (self.state * self.lcg_m + self.lcg_c) % self.lcg_n
        return self.state

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(functools.reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)

it = 8
bits = 512
seed = 211286818345627549183608678726370412218029639873054513839005340650674982169404937862395980568550063504804783328450267566224937880641772833325018028629959635

y = open("dump.txt", "r").read().split('\n')
y = [int(i) for i in y if i != '']

n, m ,c = crack_unknown_modulus(y)

rsa = RSA.import_key(open("public.pem", "r").read())
e = rsa.e

lcg = LCG(seed, m, c, n)

primes_arr = []
primes_n = 1
while True:
    for i in range(it):
        while True:
            prime_candidate = lcg.next()
            if not isPrime(prime_candidate):
                continue
            elif prime_candidate.bit_length() != bits:
                continue
            else:
                primes_n *= prime_candidate
                primes_arr.append(prime_candidate)
                break
    
    # Check bit length
    if primes_n.bit_length() > 4096:
        print("bit length", primes_n.bit_length())
        primes_arr.clear()
        primes_n = 1
        continue
    else:
        break
    
n = 1
for j in primes_arr:
    n *= j
print("[+] Public Key: ", n)
print("[+] size: ", n.bit_length(), "bits")

phi = 1
for k in primes_arr:
    phi *= (k - 1)

d = pow(e, -1, phi)

print("[+] Private Key: ", d)
print("[+] size: ", d.bit_length(), "bits")

with open("flag.txt", "rb") as f:
    flag = f.read()
    c = int.from_bytes(flag, "little")

m = pow(c, d, n)

print(long_to_bytes(m).decode())