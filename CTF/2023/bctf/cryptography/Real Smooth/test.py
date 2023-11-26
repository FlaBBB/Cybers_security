from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import string
import random
from pwn import xor

def encrypt(key, nonce, plaintext):
    plaintext = plaintext.ljust(18)
    chacha = ChaCha20.new(key=key, nonce=nonce)
    return chacha.encrypt(plaintext)

key = get_random_bytes(32)
nonce = get_random_bytes(8)
# m1 = b"abcddaasaa"
# m2 = b"erwfaasfaa"
# m3 = b"hkue3643aa"
# c1 = encrypt(key, nonce, m1)
# c2 = encrypt(key, nonce, m2)
# c3 = encrypt(key, nonce, m3)
# print(f"{c1 = }")
# print(f"{c2 = }")
# print(f"{c3 = }")
# print(f"{key = }")
# print(f"{nonce = }")

# attack1 = xor(c1, c2).strip(b"\x00")
# attack2 = xor(c1, c3).strip(b"\x00")
# attack3 = xor(c2, c3).strip(b"\x00")
# print(f"{attack1.hex() = }")
# print(f"{attack2.hex() = }")
# print(f"{attack3.hex() = }")
# print(xor(attack1, m2))
# print(xor(attack1, m1))
# print(xor(attack2, m1))
# print(xor(c1, m1.ljust(18)))
# print(xor(c2, m2.ljust(18)))
# print(xor(c3, m3.ljust(18)))

# print(xor(attack1, attack2).hex())

# print("+----------------------------------------------------+")

# m1 = b"aaaaaaa"
# m2 = b"bbbbbbb"
# c1 = encrypt(key, nonce, m1)
# c2 = encrypt(key, nonce, m2)
# print(f"{c1 = }")
# print(f"{c2 = }")

# attack = xor(c1, c2).strip(b"\x00")[:-1]
# print(f"{attack = }")
# print(xor(attack, m1))
# print(xor(attack, m2))
# print(xor(c1, m1))
# print(xor(c2, m2))

# ===========================================================================

def gen_random_string(length):
    return "".join(random.choice(string.ascii_letters + string.digits + string.punctuation + " ") for _ in range(length))

m = gen_random_string(18).encode()
c = encrypt(key, nonce, m)
xor_key = xor(c, m)

for i in range(1000):
    m = gen_random_string(18).encode()
    c = encrypt(key, nonce, m)
    assert xor(c, m) == xor_key