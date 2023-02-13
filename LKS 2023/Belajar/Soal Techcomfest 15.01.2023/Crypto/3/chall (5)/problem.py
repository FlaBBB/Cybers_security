from random import randint
from Crypto.Util.number import *

def faktorterbesar(a,b): return faktorterbesar(b%a,a) if a else b

def totient(numbers):
    totient = 1
    #########################################################
    #                                                       #
    # lah kok ilang? pasti gara gara ketumpahan kopi        #
    # padahal udah sulit sulit buat fungsi EULER TOTIENT :( #
    #                                                       #
    #########################################################
    return totient

def cari_e():
    while True:
        e = randint(57331,65537)
        if faktorterbesar(e,(p-1)*(q-1)) == 1:
            if faktorterbesar(e,n) == 1:
                return e
        else:
            continue

flag = b'TECHCOMPFEST2023{###REDACTED###}'
flag = bytes_to_long(flag)

p = getPrime(256)
q = getPrime(256)
n = p*q

e = cari_e()
e1 = e % (6*3 + 1)
e2 = e % (6*13 + 1)
e3 = e % (6*31 + 1)

minpminq = -p -q

c = pow(flag, e, n)
ne = n * pow(e,p*2,p)
kunci = totient(6^1337^totient(7))
ckunci = c^kunci

print('e1 =', e1)
print('e2 =', e2)
print('e3 =', e3)
print('minpminq =', minpminq)
print('ne =', ne)
print('cxorkunci =', ckunci)
print('totienttest =', totient(11), totient(27), totient(211))