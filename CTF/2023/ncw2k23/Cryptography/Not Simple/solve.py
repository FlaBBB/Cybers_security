from sage.all import PolynomialRing, Zmod, ceil, floor
from Crypto.Util.number import *
from pwn import *
from randcrack import RandCrack
from gmpy2 import iroot

# nc 103.145.226.209 1928
HOST = "103.145.226.209"
PORT = 1928

io = remote(HOST, PORT)

class predict_wow:
    def __init__(self, io):
        self.crack_random = RandCrack()
        self.io = io
        main()

    def get_wow(self):
        self.io.sendlineafter(b">>", b"1")
        wadidaw = int(io.recvline().strip().split(b"= ")[-1], base=16)
        return [wadidaw >> (128*pow(2,i)) & int("0b" + ("1" * 32), 2) for i in range(0, 4)]

    def main(self) -> RandCrack: 
        for _ in range(624//4):
            for w in self.get_wow():
                self.crack_random.submit(w)
        return self.crack_random

def low_e_attack(n,e,c):
    root_c = iroot(c, e)
    while not root_c[1]:
        c += n
        root_c = iroot(c, e)
    return root_c[0]

def main():
    e = 17
    io.sendlineafter(b"Masukkan e =", str(e).encode())
    predicting = predict_wow(io)

if __name__ == "__main__":
    main()