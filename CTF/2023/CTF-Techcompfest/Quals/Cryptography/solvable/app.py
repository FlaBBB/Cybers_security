from Crypto.Util.number import *

flag = "YOKOSO_KIRAKIRA_DOKIDOKI_MOCHIMOCHI_PUYOPUYO_WAKUWAKU_WASHOI"
N = 0x11B4C225F4DC385553FAEF71FD12D7A7D3731EEBB47D01DF2BD9C06CC95D67D933A3867DC3EF17547AE5A969DBC985489A3E835DDB0F8E1EB82B2CB84A5B168F74A808A0B7ACCBC1513CD416A5E8A4055A2823E192BDBE5DA3583B11B0A1697A5A47


def able(s):
    a = inverse(e, N)
    b = pow(a, 2, N)
    res = (pow(e, s, N) + pow(a, s, N) + pow(b, s, N)) % N
    return res


def solv(nbit):
    pbit = nbit // 3
    p, q, r = [getPrime(pbit) for _ in range(3)]
    return p * q * r, able((q * r) % (1 << pbit))


m = bytes_to_long(flag.encode())
e = 65537
n, u = solv(1536)  # n = p*q*r, s = (q*r) % (1 << pbit), u = e^s + e^-s + e^-2s (mod n)
c = pow(m, e, n)

print(f"{n = }\n{u = }\n{c = }")
