from PIL import Image
import numpy as np
cp = open("enc").read().split("\n\n")

pixel = []
length_x = None
for c in cp:
    c1 = c.split("+")
    temp = []
    for x in c1:
        c2 = x.strip().split("x")
        if c2[0] == '1':
            appended = 0xff
        else:
            appended = 0x00
        for _ in range(int(c2[1])):
            if length_x != None and len(temp) >= length_x:
                break
            temp.append((appended,appended,appended))
    if length_x == None:
        length_x = len(temp)
    pixel.append(temp)
    
array = np.array(pixel, dtype=np.uint8)

new_image = Image.fromarray(array)
new_image.save('new.png')