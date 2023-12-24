from libnum import s2n
from Crypto.Util.number import getPrime
from secret import flag

def encrypt(val):
    Set = [getPrime(1024),getPrime(1024)]
    p = getPrime(1024)
    n = pow(2,3) + pow(2,4)
    x = Set[0] + Set[1]
    y = pow(Set[0], len(Set)) + pow(Set[1], len(Set))
    z = Set[0] * Set[1] + pow(p,2,n)

    val = s2n(val)
    enc = (val ^ (Set[0]**3 + Set[1]**3)) * (x + y)
    enc = hex(enc)[2:]
    return [x,z,enc]

if __name__ == '__main__':
    enc = encrypt(flag)
    open('output.txt', 'w').write('')
    for i in enc:
        open('output.txt', 'a').write(str(i) + '\n')