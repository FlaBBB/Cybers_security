import math

def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen: return False
        seen.add(x)
    return True

def fermat(n):
    assert n % 2 != 0
    a = math.ceil(math.sqrt(n))
    b2 = a * a - n
    while not is_square(b2):
        a += 1
        b2 = a * a - n
    return a - math.sqrt(b2), a + math.sqrt(b2)


# test
print(fermat(2345678917))