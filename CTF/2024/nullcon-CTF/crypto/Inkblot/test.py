from Crypto.PublicKey import ECC

loaded_pem = open("ecdsa_test_conv").read()
key = ECC.import_key(loaded_pem)
print(key)
