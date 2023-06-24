from math import sqrt, ceil
from decimal import Decimal
p = 29
ints = [14, 6, 11]

print("p = ",p)
residue = []
for r in range(1, ceil(p/2)):
    res = pow(r,2,p)
    if res not in residue:
        residue.append(res)
print("list residue of p :")
print(residue)

for c in ints:
    print()
    if c not in residue:
        print(str(c)+" is non-residue")
        print("result: -1")
    else:
        print(str(c)+" is residue")
        c = c % p
        for x in range (2, p):
            if ((x * x) % p == c) :
                print( "Result: ", x)
                break