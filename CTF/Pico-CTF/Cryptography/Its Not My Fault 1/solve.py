from pwn import *
from math import gcd
import random
from multiprocessing import Pool
from functools import partial

HOST = "mercury.picoctf.net"
PORT = 10055

BITS = 20
MAX_RANGE = 1 << BITS

def md5_bruteforce(m_start, h_end):
    i = 0
    while True:
        m = m_start + str(i)
        if hashlib.md5(m.encode()).hexdigest()[-len(h_end):] == h_end:
            return m
        i += 1

def calculate_p(dp, m, n, e):
    p = gcd(m - pow(m, e * dp, n), n)
    if p > 1:
        return True, (p, n // p)
    return False, dp

def bruteforce(m, n, e, num_process = 6):
    _calculate_p = partial(calculate_p, m = m, n = n, e = e)
    pool = Pool(num_process)
    for return_val in pool.imap(_calculate_p, range(MAX_RANGE), chunksize=1000):
        if return_val[0]:
            return return_val[1]
        elif return_val[1] % 1000 == 0:
            percent_complete = (return_val[1] / MAX_RANGE) * 100
            print("\rBruteforcing RSA-CRT d_p: " + str(round(percent_complete, 2)) + "%", end = "        ")


def main():
    io = connect(HOST, PORT)

    buffer = io.recvline().decode().strip()

    m_start = buffer.split('"')[1]
    h_end = buffer.split(':')[1].strip()
    
    print("Bruteforce md5 with:")
    print("message start: " + m_start)
    print("hash end: " + h_end)

    md5 = md5_bruteforce(m_start, h_end)
    print("Found md5: " + md5)
    io.sendline(md5.encode())

    n = int(io.recvline().decode().split(':')[1].strip())
    e = int(io.recvline().decode().split(':')[1].strip())

    print("n: " + str(n))
    print("e: " + str(e))

    m = random.randint(1000, 100000)

    print("using m: " + str(m))

    print("Bruteforcing RSA-CRT d_p", end = "")

    p, q = bruteforce(m, n, e)
    print(f"\nFound p = {p} \nq = {q}")

    io.sendline(str(p + q).encode())
    io.interactive()

if __name__ == "__main__":
    main()