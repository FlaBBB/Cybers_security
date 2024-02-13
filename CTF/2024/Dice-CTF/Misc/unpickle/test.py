from Crypto.Util.number import *

m = "105110105652100972108977103110121974"

res = ""
c = ""
for i in range(0, len(m), 3):
    c += m[i : i + 3]
    print(i, m[i : i + 3], end=" ")
    if i not in [0, 6, 12, 18, 24, 30]:
        c = chr(int(c))
        print(c.encode())
        res += c
        c = ""
    else:
        print()

print(res.encode())
print("emoji")
for c in "🤩😫😩🥺🥹😭😙😘😍🥰❤🫶🤍🩷":
    print(c.encode(), ord(c))
