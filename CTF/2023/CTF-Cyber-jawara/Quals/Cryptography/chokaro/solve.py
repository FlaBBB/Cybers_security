import numpy as np
from PIL import Image
from itertools import product
from pyzbar.pyzbar import decode

def rescale(arr):
    mod = len(arr)
    final_arr = np.zeros(shape=(mod*10,mod*10), dtype=bool)
    for i in range(mod):
        for j in range(mod):
            final_arr[i*10:(i+1)*10, j*10:(j+1)*10] = arr[i][j]

    return final_arr

def descale(arr):
    mod = len(arr)
    final_arr = np.zeros(shape=(mod//10,mod//10), dtype=bool)
    for i in range(mod//10):
        for j in range(mod//10):
            final_arr[i][j] = arr[i*10][j*10]

    return final_arr
    
def demix(a, b, arr):
    mod = len(arr)
    narr = np.zeros(shape=(mod,mod), dtype=bool)
    for (x,y), _ in np.ndenumerate(arr):
        nx = (x + y * a) % mod
        ny = (x * b + y * (a * b + 1)) % mod

        narr[x][y] = arr[nx][ny]
    
    return narr

def validate_qr(arr):
    decoded = decode(invert_image(arr).astype(np.uint8) * 255)
    if decoded:
        print(decoded[0].data.decode())
        return True
    else:
        return False

def demix_brute(arr):
    mod = len(arr)
    for a, b in product(range(1, mod), repeat=2):
        narr = arr
        for _ in range(22):
            narr = demix(a, b, narr)
        if validate_qr(rescale(narr)):
            break

def invert_image(arr):
    return np.logical_not(arr)

img = Image.open('mixed.png')
arr = np.asarray(img)
arr = descale(arr)

demix_brute(arr)
