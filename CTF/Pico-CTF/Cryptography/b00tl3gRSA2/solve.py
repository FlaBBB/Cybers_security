from pwn import *
from attacks.rsa.wiener_attack import attack
from Crypto.Util.number import long_to_bytes

HOST = "jupiter.challenges.picoctf.org"
PORT = 18243

def main():
    io = connect(HOST, PORT)
    
    c = int(io.recvline().decode().split(':')[1].strip())
    n = int(io.recvline().decode().split(':')[1].strip())
    e = int(io.recvline().decode().split(':')[1].strip())
    
    print("c: " + str(c))
    print("n: " + str(n))
    print("e: " + str(e))
    
    print("Attacking with Wiener attack...")
    
    *factor, d = attack(n, e)
    print("Attack success!")
    print("Found factor: " + str(factor))
    print("Found d: " + str(d))
    
    M = pow(c, d, n)
    print("Flag:", long_to_bytes(M).decode())

if __name__ == "__main__":
    main()