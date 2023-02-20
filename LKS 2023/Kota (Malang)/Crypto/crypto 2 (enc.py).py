#!usr/bin/python3

def encrypt(plaintext):
    plaintext = plaintext[::-1]
    ciphertext = ""
    for i in plaintext:
        copy = "X" * ((ord(i) ^ 0x50) + 9)
        copy += "-"
        ciphertext += copy
    return ciphertext

print ("Jatim Encryptor")
plaintext = input("Masukkan string yang ingin di-encrypt: ")
print ("Result : ")
print (encrypt(plaintext))