from itertools import product

from Crypto.Util.number import getPrime


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


p = getPrime(512)
q = getPrime(512)
N = p * q

_p = [x if i % 2 == 0 else "?" for i, x in enumerate(str(p))]
_q = [x if i % 2 == 1 else "?" for i, x in enumerate(str(q))]
print(p)
print(q)
print("".join(_p))
print("".join(_q))
if (_p[-1] == "?" and _q[-1] == "?") or (_p[-1] != "?" and _q[-1] != "?"):
    print(solving(_p, _q, N, True))
else:
    print(solving(_p, _q, N))
print()
