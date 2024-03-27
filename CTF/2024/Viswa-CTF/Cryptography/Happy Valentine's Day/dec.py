from itertools import cycle

from PIL import Image


def xor(a, b):
    return [i ^ j for i, j in zip(a, cycle(b))]


f = open("enc.txt", "rb").read()
key = [137, 80, 78, 71, 13, 10, 26, 10]

enc = bytearray(xor(f, key))


open("original.png", "wb").write(enc)
