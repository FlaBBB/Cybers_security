import this
input_peserta = input('Yuk belajar bahasa ular yang sudah di-"goreng"!\nMasukkan nama file kamu dan kami mengubahnya menjadi format yang keren! >>')
f_handler = open(input_peserta, 'rb').read()
f_transform = []
for karakter in f_handler:
    f_transform.append(karakter ^ 2 ^ 3 ^ 7 ^ 9 ^ 11 ^ 13)
else:
    f_final = ''
    for karakterlagi in range(len(f_transform)):
        f_final += chr(f_transform[karakterlagi] ^ ord(this.s[karakterlagi % len(f_transform)]))
    else:
        with open(input_peserta+'.dec', 'wb') as (hehe):
            hehe.write(f_final.encode())
            hehe.close()
        print('NOICE!!!')