#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret import flag
import os

KEY = AES.get_random_bytes(16)

def enc(plaintext):
    plaintext = bytes.fromhex(plaintext)
    salt = os.urandom(8)
    padded = pad(plaintext + salt + flag.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded)
    return encrypted.hex()

def dec(ciphertext):
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(bytes.fromhex(ciphertext))
    unpadded = unpad(decrypted,16)
    plaintext = unpadded.rstrip(flag.encode())[:-8]
    return plaintext.decode()

menu = ['----- Layanan enkripsi pesan -----','Meskipun sistem enkripsi jadoel, tapi harusnya masih aman!','[1] Enkrip pesan','[2] Dekrip Pesan','[3] Keluar']
if __name__ == '__main__':
    while True:
        for i in menu:
            print(i)

        pilih = int(input('Masukkan pilihan: '))
        if pilih == 1:
            ptx = input("Masukkan pesan: ")
            ctx = enc(ptx)
            print('Hasil enkripsi:',ctx)
        elif pilih == 2:
            c_ctx = input("Masukkan pesan terenkripsi: ")
            p_ptx = dec(c_ctx)
            print('Hasil dekripsi:',p_ptx)
        elif pilih == 3:
            print("Cya!")
            break
        else:
            print("Pilihan salah!")