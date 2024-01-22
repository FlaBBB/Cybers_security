from Crypto.Util.number import inverse

p = 9739
a = 497
b = 1768


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

P = (493, 5564)
Q = (1539, 4742) 
R = (4403,5202)

S = point_addition(point_addition(point_addition(P, P), Q), R)
print(S)