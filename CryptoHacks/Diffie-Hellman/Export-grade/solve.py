from pwn import *
from Crypto.Util.number import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from math import ceil, sqrt

def bsgs(g, y, p):
    """
    Reference:

    To solve DLP: y = g^x % p and get the value of x.
    We use the property that x = i*m + j, where m = ceil(sqrt(n))

    :parameters:
        g : int/long
                Generator of the group
        y : int/long
                Result of g**x % p
        p : int/long
                Group over which DLP is generated. Commonly p is a prime number

    :variables:
        m : int/long
                Upper limit of baby steps / giant steps
        x_poss : int/long
                Values calculated in each giant step
        c : int/long
                Giant Step pre-computation: c = g^(-m) % p
        i, j : int/long
                Giant Step, Baby Step variables
        lookup_table: dictionary
                Dictionary storing all the values computed in the baby step
    """
    mod_size = len(bin(p-1)[2:])

    print("[+] Using BSGS algorithm to solve DLP")
    print("[+] Modulus size: " + str(mod_size) + ". Warning! BSGS not space efficient\n")

    m = ceil(sqrt(p-1))
    # Baby Step
    lookup_table = {pow(g, j, p): j for j in range(m)}
    # Giant Step pre-computation
    c = pow(g, m*(p-2), p)
    # Giant Steps
    for i in range(m):
        temp = (y*pow(c, i, p)) % p
        if temp in lookup_table:
            # x found
            return i*m + lookup_table[temp]
    return None

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
# socket.cryptohack.org 13379
io = remote('socket.cryptohack.org', 13379)

io.sendlineafter(b"Bob", b"{\"supported\": [ \"DH64\"]}")
io.sendlineafter(b"Alice", b"{\"chosen\": \"DH64\"}")
recv = io.recvall().split(b"\n")
print(recv)
recv_A = json.loads(recv[0].split(b"Alice:")[1].strip())
recv_B = json.loads(recv[1].split(b"Bob:")[1].strip())
enc = json.loads(recv[2].split(b"Alice:")[1].strip())
p = int(recv_A["p"], 16)
g = int(recv_A["g"], 16)
A = int(recv_A["A"], 16)
a = bsgs(2, A, p)

B = int(recv_B["B"], 16)
k = pow(B, a, p)

flag = decrypt_flag(k, enc["iv"], enc["encrypted_flag"])
print(flag)