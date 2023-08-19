from Crypto.Util.number import getPrime, inverse, bytes_to_long
from string import ascii_letters, digits
from random import choice

pride = "".join(choice(ascii_letters + digits) for _ in range(16))
gluttony = getPrime(128) # p
greed = getPrime(128) # q
lust = gluttony * greed # n
sloth = 65537 # e
envy = inverse(sloth, (gluttony - 1) * (greed - 1)) # d

anger = pow(bytes_to_long(pride.encode()), sloth, lust) # c

print(f"{anger = }")
print(f"{envy = }")

print("vainglory?")
vainglory = input("> ").strip()

if vainglory == pride:
    print("Conquered!")
    with open("/challenge/flag.txt") as f:
        print(f.read())
else:
    print("Hubris!")
