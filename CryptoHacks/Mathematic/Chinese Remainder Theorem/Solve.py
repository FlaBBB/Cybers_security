import math

def chinese_remainder_theorem(remainders, moduli, trashed = []):
    assert len(remainders) > 1
    assert len(remainders) == len(moduli)
    
    product_of_moduli = math.prod(moduli)

    solution = 0
    for i in range(len(remainders)):
        Mi = product_of_moduli // moduli[i]
        gcd, inverse, _ = extended_euclidean_algorithm(Mi, moduli[i])
        if gcd != 1:
            return chinese_remainder_theorem(remainders[:i] + remainders[i + 1:], moduli[:i] + moduli[i + 1:], trashed + [i])
        solution += remainders[i] * inverse * Mi

    return solution % product_of_moduli, product_of_moduli, trashed

def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = extended_euclidean_algorithm(b, a % b)
        return gcd, y, x - (a // b) * y

a = [2,3,5]
N = [5,11,17]


res = chinese_remainder_theorem(a, N)
print(res)