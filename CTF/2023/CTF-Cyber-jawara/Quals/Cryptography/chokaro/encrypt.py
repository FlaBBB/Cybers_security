import random
import numpy as np
import qrcode
from PIL import Image

def mix(a,b,arr):
    mod = len(arr)
    narr = np.zeros(shape=(mod,mod), dtype=bool)
    for (x,y), element in np.ndenumerate(arr):
        nx = (x + y * a) % mod
        ny = (x * b + y * (a * b + 1)) % mod

        narr[nx][ny] = element
        assert narr[nx][ny] == arr[x][y]

    return narr

def rescale(arr):
    mod = len(arr)
    final_arr = np.zeros(shape=(mod*10,mod*10), dtype=bool)
    for i in range(mod):
        for j in range(mod):
            final_arr[i*10:(i+1)*10, j*10:(j+1)*10] = arr[i][j]

    return final_arr

FLAG = open('flag.txt', 'r').read()

qr = qrcode.QRCode(border=0)
qr.add_data(FLAG)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img.save('qr.png')

mat = np.array(qr.get_matrix(), dtype=bool)

print(len(mat))
a = random.randrange(1, len(mat)-1)
b = random.randrange(1, len(mat)-1)

scrambled = mat
for _ in range(22):
    scrambled = mix(a,b,scrambled)

scrambled = rescale(scrambled)

img = Image.fromarray(scrambled)
img.save('mixedNrescale_test.png')