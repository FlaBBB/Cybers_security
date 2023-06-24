g = 3
p = 13
c = 1

print("g * d === c (mod p)  --  `===` is equivalent")
print()
print("g = ", g)
print("c = ", c)
print("p = ", p)
print("get d")
print()
if c >= p:
    print("c cannot more than p")
else:
    pt = p
    while True:
        if (pt+c) % g == 0:
            print("result: ", end="")
            print(str((pt+c)//g))
            break
        pt += p
