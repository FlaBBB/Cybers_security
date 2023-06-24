from OpenSSL.crypto import load_certificate, FILETYPE_PEM

with open("2048b-rsa-example-cert_3220bd92e30015fe4fbeb84a755e7ca5.der","rb") as fp:
    cert = load_certificate(FILETYPE_PEM, fp.read())

modn = cert.get_pubkey().to_cryptography_key().public_numbers().n

# Convert it to hex
print('{:X}'.format(modn))
