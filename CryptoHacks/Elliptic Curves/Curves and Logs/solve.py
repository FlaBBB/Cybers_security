from Crypto.Util.number import inverse

p = 9739
a = 497
b = 1768


def eliptic(x, y):
    _x = (x**3 + a * x + b) % p
    _y = (y**2) % p
    assert _x == _y, "Not on curve, x: {}, y: {}".format(x, y)
    return _x


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


G = (1804, 5368)

QA = (815, 3190)
nB = 1829
print((815*nB)%p)

S = scalar_multiplication(nB, QA)
print(S)

from hashlib import sha1

print(sha1(str(S[0]).encode()).hexdigest())
