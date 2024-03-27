from math import floor
from random import randrange

from Crypto.Cipher import AES
from Crypto.Util.number import getPrime  # https://pypi.org/project/pycryptodome/
from Crypto.Util.Padding import pad


def lcg(s, a, b, p):
    return (a * s + b) % p


p = getPrime(floor(72.7))
a = randrange(0, p)
b = randrange(0, p)
seed = randrange(0, p)
print(f"{p = }")
print(f"{a = }")
print(f"{b = }")


def get_roll():
    global seed
    seed = lcg(seed, a, b, p)
    return seed % 100


out = []
raw_out = []
for _ in range(floor(72.7)):
    out.append(get_roll())
    raw_out.append(seed)
print(f"{out = }")
print(f"{raw_out = }")

# flag = open("flag.txt", "rb").read()
# key = bytes([get_roll() for _ in range(16)])
# iv = bytes([get_roll() for _ in range(16)])
# cipher = AES.new(key, AES.MODE_CBC, iv)
# print(cipher.encrypt(pad(flag, 16)).hex())
