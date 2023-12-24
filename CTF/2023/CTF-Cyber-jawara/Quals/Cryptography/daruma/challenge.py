import random
from Crypto.Util.number import *


class AECF:
    def __init__(self, p=None, q=None, g=2):

        p = p or getPrime(512)
        q = q or getPrime(512)
        n = p * q
        self.g = g
        self.n2 = n**2
        self.totient = n * (p - 1) * (q - 1)

        while True:
            self.k = random.randrange(2, self.n2 - 1)
            if GCD(self.k, self.n2) == 1:
                break

        while True:
            self.e = random.randrange(2, self.totient - 1)
            if GCD(self.e, self.totient) == 1:
                break

        self.d = inverse(self.e, self.totient)

        self.l = random.randrange(1, self.n2 - 1)
        self.beta = pow(self.g, self.l, self.n2)

    def public_key(self):
        return (self.n2, self.e, self.beta)
    
    def private_key(self):
        return (self.d, self.l)

    def encrypt_and_sign(self, plaintext, public):

        n2, e, beta = public

        m = bytes_to_long(plaintext)

        r = pow(self.k, e, n2) % n2
        s = m * self.k * pow(beta, self.l, n2) % n2

        return r, s

    def decrypt_and_verify(self, r, s, beta):

        m = s * inverse(pow(r, self.d, self.n2), self.n2) * \
            inverse(pow(beta, self.l, self.n2), self.n2) % self.n2

        return long_to_bytes(m)

FLAG = open('flag.txt', 'rb').read()
bob = AECF()

enc_flag = bob.encrypt_and_sign(FLAG, bob.public_key())
assert bob.decrypt_and_verify(*enc_flag, bob.beta) == FLAG

print("Encrypted flag:", enc_flag)
print("Bob public key:", bob.public_key())

for _ in range(2):
    print()
    print("="*40)
    try:
        n = int(input("Your public modulus: "))
        if n.bit_length() < 2000 or n.bit_length() > 10000 or isPrime(n):
            print("Insecure modulus")
            break

        e = int(input("Your public e: "))
        beta = int(input("Your public beta: "))
        message = input("Message you want to encrypt and sign: ")

        c = bob.encrypt_and_sign(message.encode(), (n, e, beta))
        print("Your ciphertext:", c)

    except Exception as e:
        print(e)
        break