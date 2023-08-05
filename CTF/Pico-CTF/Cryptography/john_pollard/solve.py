from Crypto.PublicKey import RSA

cert = RSA.importKey(open("cert").read())

n = cert.n
e = cert.e

print("n: " + str(n)) # 4966306421059967
print("e: " + str(e)) # 65537

# Factor from Yafu
p = 73176001
q = 67867967

print(f"Flag: picoCTF{{{p},{q}}}")