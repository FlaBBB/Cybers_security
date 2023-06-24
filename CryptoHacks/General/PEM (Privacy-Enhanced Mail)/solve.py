from Crypto.PublicKey import RSA

with open("privacy_enhanced_mail_1f696c053d76a78c2c531bb013a92d4a.pem") as PEM:
    private_key = RSA.importKey(PEM.read())
    print("d = ",private_key.d)