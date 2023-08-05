import io
from PIL import Image
from base64 import b64decode
import cv2
from pyzbar.pyzbar import decode
import requests

def fix_qr(img):
    pixdata = img.load()
    sx = img.size[0]
    sy = img.size[1]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0]+pixdata[x, y][1]+pixdata[x, y][2] <= 255*2:
                if sx > x:
                    sx = x
                if sy > y:
                    sy = y
                    
    size_block = sy//2
    bx = sx
    by = sy
    for y in range(by,by + size_block*6+1, size_block):
        for x in range(bx, bx + size_block*6+1, size_block):
            if ((x == bx + size_block or y == by + size_block) or (x == bx + size_block*5 or y == by + size_block*5)) and not ((x == bx or y == by) or (x == bx + size_block*6 or y == by + size_block*6)):
                continue
            for a in range(size_block):
                for b in range(size_block):
                    pixdata[x+b, y+a] = (0,0,0,255)

    bx = img.size[0] - sx - size_block*7
    by = sy
    for y in range(by,by + size_block*6+1, size_block):
        for x in range(bx, bx + size_block*6+1, size_block):
            if ((x == bx + size_block or y == by + size_block) or (x == bx + size_block*5 or y == by + size_block*5)) and not ((x == bx or y == by) or (x == bx + size_block*6 or y == by + size_block*6)):
                continue
            for a in range(size_block):
                for b in range(size_block):
                    pixdata[x+b, y+a] = (0,0,0,255)

    bx = sx
    by = img.size[1] - sy - size_block*7
    for y in range(by,by + size_block*6+1, size_block):
        for x in range(bx, bx + size_block*6+1, size_block):
            if ((x == bx + size_block or y == by + size_block) or (x == bx + size_block*5 or y == by + size_block*5)) and not ((x == bx or y == by) or (x == bx + size_block*6 or y == by + size_block*6)):
                continue
            for a in range(size_block):
                for b in range(size_block):
                    pixdata[x+b, y+a] = (0,0,0,255)

    return img


req = requests.get("http://challenge01.root-me.org/programmation/ch7/")
cookies = req.cookies.get_dict()
while True:
    if "img" not in req.content.decode():
        print("Flag:",req.content.decode().split("flag est ")[1].replace("\n</p></p><br/></body></html>",""))
        break
    imgstring = req.content.decode().split('<img')[1].split('>')[0].split('src="')[1].split('"')[0]
    imgstring = imgstring.split('base64,')[-1].strip()
    pic = io.StringIO()
    image_string = io.BytesIO(b64decode(imgstring))
    image = Image.open(image_string)
    image = fix_qr(image)
    image.save("temp.png")
    img=cv2.imread("temp.png")
    res = "/"+decode(img)[0].data.decode().split("/")[1]
    print("Test:",res)
    req = requests.post("http://challenge01.root-me.org/programmation/ch7/", data={"metu":res}, cookies=cookies)
    p = req.content.decode().split("<p>")[1].split("</p>")[0].replace(".<br>","")
    if p != "":
        print(f"[FAILED] {p}")