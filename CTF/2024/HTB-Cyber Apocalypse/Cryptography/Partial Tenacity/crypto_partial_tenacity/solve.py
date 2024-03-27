from itertools import product

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import *


def check_zz(a: str, b: str, n: int, mask: int):
    res = []
    swapped = False
    if "?" in a:
        a, b = b, a
        swapped = True

    for x in range(1, 10):
        _a = int(a)
        _b = int(str(x) + b[1:])
        if (_a * _b) % mask == n % mask:
            if swapped:
                _a, _b = _b, _a
            res.append((str(_a).rjust(len(a), "0"), str(_b).rjust(len(b), "0")))

    if res == []:
        b = "0" + b[1:]
        if swapped:
            a, b = b, a
        res.append((a, b))

    return res


def check_nzz(a: str, b: str, n: int, mask: int):
    res = []
    swapped = False
    if "?" not in a and "?" not in b:
        return [(a, b)]

    for x, y in product(range(0, 10), repeat=2):
        _a = int(str(x) + a[1:])
        _b = int(str(y) + b[1:])
        if (_a * _b) % mask == n % mask:
            if swapped:
                _a, _b = _b, _a
            res.append((str(_a).rjust(len(a), "0"), str(_b).rjust(len(b), "0")))

    if res == []:
        a = "0" + a[1:]
        b = "0" + b[1:]
        if swapped:
            a, b = b, a
        res.append((a, b))

    return res


def solving(_p: list, _q: list, n: int, is_nzz=False):
    check = check_nzz if is_nzz else check_zz
    max_len = max(len(_p), len(_q))
    _p = ["0"] * (max_len - len(_p)) + _p
    _q = ["0"] * (max_len - len(_q)) + _q
    res = check(_p.pop(), _q.pop(), n, 10)
    i = 1
    while _p and _q:
        a, b = _p.pop(), _q.pop()
        temp = []
        for __p, __q in res:
            temp += check(a + __p, b + __q, n, 10 ** (i + 1))
        if not temp:
            return "No solution"
        res = temp
        i += 1

    for p, q in list(map(lambda x: (int(x[0]), int(x[1])), res)):
        if p * q == n:
            return p, q

    return "No solution"


N = 118641897764566817417551054135914458085151243893181692085585606712347004549784923154978949512746946759125187896834583143236980760760749398862405478042140850200893707709475167551056980474794729592748211827841494511437980466936302569013868048998752111754493558258605042130232239629213049847684412075111663446003
ct = bytes.fromhex(
    "7F33A035C6390508CEE1D0277F4712BF01A01A46677233F16387FAE072D07BDEE4F535B0BD66EFA4F2475DC8515696CBC4BC2280C20C93726212695D770B0A8295E2BACBD6B59487B329CC36A5516567B948FED368BF02C50A39E6549312DC6BADFEF84D4E30494E9EF0A47BD97305639C875B16306FCD91146D3D126C1EA476"
)
p = "151441473357136152985216980397525591305875094288738820699069271674022167902643"
q = "15624342005774166525024608067426557093567392652723175301615422384508274269305"
e = 65537
_p = p[0] + "".join([f"?{x}" for x in p[1:]])
_q = "".join([f"?{x}" for x in q]) + "?"

print(f"_p = {_p}\n_q = {_q}")
_p = list(_p)
_q = list(_q)
if (_p[-1] == "?" and _q[-1] == "?") or (_p[-1] != "?" and _q[-1] != "?"):
    res = solving(_p, _q, N, True)
else:
    res = solving(_p, _q, N)
if res == "No solution":
    print("No solution")
    exit()
p, q = res
print(f"p = {p}\nq = {q}")
assert p * q == N

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

RSAkey = RSA.construct((p * q, e, d))
cipher = PKCS1_OAEP.new(RSAkey)

pt = cipher.decrypt(ct)
print(pt)
