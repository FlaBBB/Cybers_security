def enc(fl4g):
    enc = []
    holder1 = []
    holder2 = []

    for y, x in enumerate(fl4g):
        if y == 0:
            holder1.append(ord(x) + 1)
        else:
            holder1.append((ord(x) + holder1[y - 1]) % ((2 ** 9) << 16))
    print(holder1)

    for hh, zZ in enumerate(holder1):
        if hh == 0:
            holder2.append(holder1[hh])
        else:
            holder2.append((zZ + holder1[hh - 1]) % ((2 ** 9) << 8))
    print(holder2)
    enc = holder1 + holder2
    print(enc)

    for zz, wkwk in enumerate(enc):
        enc[zz] = chr(wkwk)
        print(enc[zz].encode())

    return ''.join(enc)

def dec(cipher):
    cipher = cipher[0:cipher[1:].find(cipher[0]) + 1]
    res = ""
    for i, c in enumerate(cipher):
        if i == 0:
            res += chr(ord(c) - 1)
        else:
            temp = ord(c) - ord(cipher[i - 1])
            if temp < 0:
                temp += ((2 ** 9) << 16)
            res += chr(temp)
    return res


with open('enc.txt', 'r', encoding="utf-8") as f:
    cipher = f.read()

print(dec(cipher))