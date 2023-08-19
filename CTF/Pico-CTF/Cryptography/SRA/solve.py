from Crypto.Util.number import long_to_bytes, isPrime
from sys import getsizeof
import itertools
import subprocess
from pwn import *

HOST = "saturn.picoctf.net"
PORT = 53200

def get_phi_candidate(d, e, check_until=100000):
    n = d * e - 1
    bit_range = list(range(d.bit_length(), (((d.bit_length() // 4) + 1) * 4) + 1))
    res = []
    i = 4
    for i in range(2, check_until):
        if n % i == 0:
            temp = n // i
            if temp.bit_length() in bit_range and getsizeof(temp) == getsizeof(d):
                res.append(temp)
    return res

def factor_candidate(n):
    proc = subprocess.Popen("yafu", stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    input_commands = ["factor({})".format(i) for i in n] + ["quit"]

    for command in input_commands:
        proc.stdin.write(command + "\n")
        proc.stdin.flush()

    output = proc.communicate()[0].split('***factors found***\n\n')[1:]
    res = []
    i = 0
    for o in output:
        if 'P' in o:
            res.append([])
            for line in o.split('ans =')[0].split('\n'):
                if 'P' in line:
                    res[i].append(int(line.split('P')[1].split(' = ')[-1]))
            i += 1

    return res

def validate_and_get_pq(candidate, bit_size=128):
    for c in candidate:
        for i in range(len(c)//2):
            for j in itertools.combinations(range(len(c)), i + 1):
                is_valid = True
                p = 1
                for k in j:
                    p *= c[k]
                    if p.bit_length() > bit_size:
                        is_valid = False
                        break
                p += 1
                if not isPrime(p):
                    is_valid = False
                if not is_valid:
                    continue
                q = 1
                for k in range(len(c)):
                    if k not in j:
                        q *= c[k]
                        if q.bit_length() > bit_size:
                            is_valid = False
                            break
                q += 1
                if not isPrime(q):
                    is_valid = False
                if is_valid:
                    return p, q

while True:
    io = remote(HOST, PORT)

    c = int(io.recvline().split(b' = ')[1])
    d = int(io.recvline().split(b' = ')[1])
    e = 65537
    phi_candidate = get_phi_candidate(d, e)
    if len(phi_candidate) > 10:
        io.close()
        continue
    print(phi_candidate)
    fac_phi_candidate = factor_candidate(phi_candidate)
    print(fac_phi_candidate)
    p, q = validate_and_get_pq(fac_phi_candidate)
    print("get p, q")
    print(f"{p = }")
    print(f"{q = }")
    n = p * q
    M = pow(c, d, n)
    M = long_to_bytes(M)
    print(f"{M = }")
    io.sendlineafter(b">", M)
    break
    
io.interactive()