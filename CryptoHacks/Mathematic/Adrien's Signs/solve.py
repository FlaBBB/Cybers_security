def legendre_symbol(a, p):
    if pow(a, (p-1)//2, p) == p-1: 
        return 0
    else:
        return pow(a, (p-1)//2, p)
    
def decrypt(cipher, p):
    temp = ''
    res = ''
    for x in cipher:
        if len(temp) >= 8:
            res += chr(int(temp, 2))
            temp = ''
        temp += str(legendre_symbol(int(x), p))
    if len(temp) >= 8:
        res += chr(int(temp, 2))
    return res

p = 1007621497415251
cipher = open('output').read().replace('[','').replace(']', '').replace(' ','').split(',')
print(decrypt(cipher, p))
