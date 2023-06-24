from Crypto.PublicKey import RSA

with open("bruce_rsa_6e7ecd53b443a97013397b1a1ea30e14.pub") as PEM:
    private_key = RSA.importKey(PEM.read())
    print("n = ",private_key.n)