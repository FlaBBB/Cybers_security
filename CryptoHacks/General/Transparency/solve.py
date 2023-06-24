from Crypto.PublicKey import RSA
from cryptography.x509 import certificate_transparency

with open("transparency_afff0345c6f99bf80eab5895458d8eab.pem") as PEM:
    # transperency = certificate_transparency.SignatureAlgorithm(PEM.read())
    # print(transperency)
    private_key = RSA.importKey(PEM.read())
    print("n = ",private_key.n)