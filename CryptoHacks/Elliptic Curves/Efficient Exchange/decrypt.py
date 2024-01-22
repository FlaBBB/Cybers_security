from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


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


iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

# ---------------------------------------------------------------------------

from Crypto.Util.number import inverse
import gmpy2

p = 9739
a = 497
b = 1768


def eliptic(x = None, y = None):
    res = 0
    if x:
        _x = x**3 + a * x + b
        res = _x
    if y:
        _y = y**2
        res = _y
    if x and y:
        assert _x % p == _y % p, "Not on curve, x: {}, y: {}".format(x, y)
        res %= p
    return res


def point_addition(P, Q):
    O = (0, 0)

    if P == O:
        return Q
    if Q == O:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == -y2:
        return O

    if P != Q:
        lamb = ((y2 - y1) * inverse(x2 - x1, p)) % p
    else:
        lamb = ((3 * x1**2 + a) * inverse(2 * y1, p)) % p

    x3 = (lamb**2 - x1 - x2) % p
    y3 = (lamb * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_multiplication(n, P):
    O = (0, 0)

    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q, Q)
        n //= 2

    return R

Q_x = 4726
nB = 6534

_y = eliptic(x=Q_x)

is_root = False
while not is_root:
    Q_y, is_root = gmpy2.iroot(_y, 2)
    _y += p
Q_y %= p

print(eliptic(Q_x, Q_y))
Q = (Q_x, Q_y)

S = scalar_multiplication(nB, Q)

shared_secret = S[0]

flag = decrypt_flag(shared_secret, iv, ciphertext)
print(flag)
