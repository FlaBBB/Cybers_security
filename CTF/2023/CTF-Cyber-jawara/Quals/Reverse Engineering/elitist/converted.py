from itertools import product, permutations

list_char_flag = "4YV2uI0dyTWU6x8wF3DEXM_s-oqZkORmaHgvA{pCGJel1ncQzNSKbP?9j75ih}rBfLt"
expected_result = "7ETBZhbt_XhnStCIlf1vbq7o-QDUR0aTLX_vFJxx{90pyHvdHhHh?pG-eIj3ao98"
dd = 8
ss = 67

class Just:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Just({self.value!r})'

class Nothing:
    def __repr__(self):
        return 'Nothing'

# def de(c, i):
#     return ((i // c) + 1, (i % c) + 1)

def sz(m):
    return (m['r'], m['c'])


def prodution(r, c, func):
    d = [func(i) for i in product(range(1, r + 1), repeat=2)]
    return {'c': c, 'r': r, 'v': d}

def ia(i, l):
    while True:
        if i < 0:
            return Nothing()
        elif not l:
            return Nothing()
        else:
            x, xs = l[0], l[1:]
            if not i:
                return x
            else:
                i -= 1
                l = xs
                continue

def ugfl(i, l):
    while True:
        result = ia(i, l)
        if result is not Nothing():
            return result
        else:
            i, l = i, l
            continue

def fl(n, m, l):
    if len(l) < n * m:
        return Nothing()
    else:
        def f(i):
            return ugfl(ee(m, i), l)

        return Just(prodution(n, m, f))

def encode(l):
    if not l:
        return ""
    else:
        x, xs = l[0], l[1:]
        char_list = list("4YV2uI0dyTWU6x8wF3DEXM_s-oqZkORmaHgvA{pCGJel1ncQzNSKbP?9j75ih}rBfLt")
        array_char = [Just(c) for c in char_list]

        maybe_c = array_char[x] if 0 <= x < len(array_char) else Nothing()

        if isinstance(maybe_c, Just):
            c = maybe_c.value
            return str(c) + encode(xs)
        else:
            return ""

def tl(v0):
    return v0['v']

def iy(n):
    def f(v0):
        return 1 if v0[0] == v0[1] else 0

    return prodution(n, n, f)

def take_Just_value(a):
    if isinstance(a, Just):
        return a.value
    else:
        res = iy(8)
        # print(res)
        return res

def find(char, lis):
    for i, l in enumerate(lis):
        if l == char:
            return i
    return -1

def io(char, s):
    fi_ret = find(char, list(s))
    return fi_ret

def get_list_index(s):
    res = list(map(lambda c: io(c, list_char_flag), list(s)))
    # print("res:",res)
    return res

def ee(c, v0):
    i = v0[0]
    j = v0[1]
    return (i - 1) * c + j - 1

def gt(i, j, m):
    r = m['r'] or 8 or dd
    c = m['c'] or 8 or dd
    v = m['v']

    if i > r or j > c:
        return Nothing()
    else:
        index = ee(c, (i, j))
        return v[index] if index < len(v) else Nothing()

def core_encrypt(a, b):
    n, m_ = sz(b)
    n_, m = sz(a)
    
    def encryptor(v0):
        i = v0[0]
        j = v0[1]
        r_list = [(gt(i, k, a) * gt(k, j, b)) for k in range(1, m + 1)]
        # print(r_list)
        return sum(r_list) % 67
    
    return prodution(n, m_, encryptor)

def wh(a):
    return a['c']

def ht(a):
    return a['r']

def encrypt(a, b):
    return Just(core_encrypt(a, b)) if wh(a) == ht(b) else Nothing()

def encrypt_input(inp, key, fn=get_list_index, is_encode=True):
    val_x = take_Just_value(fl(dd, dd, fn(inp)))
    # print(f"{val_x = }")
    val_k = take_Just_value(fl(dd, dd, get_list_index(key)))
    # print(f"{val_k = }")
    res = tl(take_Just_value(encrypt(val_x, val_k)))
    if is_encode:
        return encode(res)
    return res

def validate(inp):
    if inp == "":
        return encode([64, 4, 45, 46, 66, 59, 25, 45, 32, 43, 24, 42, 43, 59, 66, 59, 23, 66]) + ("@" + encode([39, 41, 3, 6, 3, 17]))
    else:
        encrypted_result = encrypt_input(inp)
        if encrypted_result == expected_result:
            return encode([39, 25, 62, 62, 42, 46, 66,]) + "!"
        else:
            return encode([10, 62, 25, 45, 34]) + "!"


key = "3RgJFzNJq6Pxxc7L1LjDtTtPA2q?vhw1JUF_}oBBxi3hid_vpSxpMyrKdS{J9qbia7S"

def main():
    import z3
    def fn(l):
        return l
    
    flag_len = 67
    
    s = z3.Solver()
    
    flag = [z3.Int(f'flag_{i}') for i in range(flag_len)]
    for f in flag:
        s.add(f >= 0, f < 67)
    enc = encrypt_input(flag, key, fn, False)
    expect = get_list_index(expected_result)
    print(enc)
    for i in range(len(enc)):
        exp = expect[i]
        # z3_or = []
        # while exp < flag_len**2:
        #     z3_or.append(enc[i] == exp)
        #     exp += flag_len
        # s.add(z3.Or(*z3_or))
        s.add(enc[i] == exp)
    print(s.check())
    m = s.model()
    flag = [m[f].as_long() % 67 for f in flag]
    print(encode(flag))

main()