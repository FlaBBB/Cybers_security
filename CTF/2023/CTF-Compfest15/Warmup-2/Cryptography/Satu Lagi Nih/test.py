from Crypto.Util.number import *
import gmpy2
from math import isqrt, gcd
import primefac

def is_square(x):
    """
    Returns the square root of x if x is a perfect square, or None otherwise.
    :param x: x
    :return: the square root of x or None
    """
    y = isqrt(x)
    return y if y ** 2 == x else None

def factorize(N):
    """
    Recovers the prime factors from a modulus using Fermat's factorization method.
    :param N: the modulus
    :return: a tuple containing the prime factors, or None if the factors were not found
    """
    a = isqrt(N)
    b = a * a - N
    while b < 0 or not is_square(b):
        a += 1
        b = a * a - N

    p = a - isqrt(b)
    q = N // p
    if p * q == N:
        return p, q
    
def factorize_2(N1, N2):
    assert N1 < N2
    t_N1 = N1
    while True:
        if gcd(t_N1, N2) != 1: break
        t_N1 += 1
    p = gcd(t_N1, N2)
    q = N2 // p
    if (N1 // gmpy2.next_prime(p)) * gmpy2.next_prime(p) == N1:
        r = gmpy2.next_prime(p)
    elif (N1 // gmpy2.next_prime(q)) * gmpy2.next_prime(q) == N1:
        r = gmpy2.next_prime(q)
    else:
        raise Exception("Something wrong!")
    s = N1 // r
    return p, q, r, s

def factorize_3(N1, N2):
    a = isqrt(N1)
    b = N1 // a
    while gcd(a * b, N2) == 1:
        a -= 1
        b = N1 // a
    p = gcd(a * b, N2)
    q = N2 // p
    if (N1 // gmpy2.next_prime(p)) * gmpy2.next_prime(p) == N1:
        r = gmpy2.next_prime(p)
    elif (N1 // gmpy2.next_prime(q)) * gmpy2.next_prime(q) == N1:
        r = gmpy2.next_prime(q)
    else:
        raise Exception("Something wrong!")
    s = N1 // r
    return p, q, r, s

def factorize_3(N1, N2):
    a = isqrt(N1)
    b = N1 // a
    while gcd(a * b, N2) == 1:
        a -= 1
        b = N1 // a
    p = gcd(a * b, N2)
    q = N2 // p
    if (N1 // gmpy2.next_prime(p)) * gmpy2.next_prime(p) == N1:
        r = gmpy2.next_prime(p)
    elif (N1 // gmpy2.next_prime(q)) * gmpy2.next_prime(q) == N1:
        r = gmpy2.next_prime(q)
    else:
        raise Exception("Something wrong!")
    s = N1 // r
    return p, q, r, s

p0 = getPrime(50)
q0 = getPrime(50)
# p0 = 73
# q0 = 101
p1 = gmpy2.next_prime(p0)
q1 = gmpy2.next_prime(q0)

n1 = p0*p1*q0*q1
pp = p1*p0
print(p0, q1)
print(q0, p1)
print(3, p0*p1, q0*q1)
print(4, p0 * q0, q1 * p1)
print(n1)

P = factorize(n1)
print(P)
print(P[1] - P[0], P[1] + P[0])
# print((P[1] + P[0]) // (P[1] - P[0]))
print(P[0] - p0 * q0)
# x = isqrt(P[1] - P[0])
# # print(pollard_p(P[1], P[1] - P[0]))
# print(factorize_3(P[0], P[1]))
# print(primefac.ecm(P[1]))
# print(gcd(P[0], P[1]))
print(factorize_3(P[0], P[1]))
