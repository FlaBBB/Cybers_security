from PIL import Image
import base64
import io
import pytesseract
import requests

def breaker(img, threshold=100):
    # clean the image
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pixdata[x, y][0] <= threshold) \
                    and (pixdata[x, y][1] <= threshold) \
                    and (pixdata[x, y][2] <= threshold) :
                if pixdata[x, y-1][0]+pixdata[x, y-1][1]+pixdata[x, y-1][2] > pixdata[x-1, y][0]+pixdata[x-1, y][1]+pixdata[x-1, y][2] and pixdata[x, y-1][0]+pixdata[x, y-1][1]+pixdata[x, y-1][2] > 255*3-100:
                    pixdata[x, y] = (pixdata[x, y-1][0],pixdata[x, y-1][1],pixdata[x, y-1][2],255)
                else:
                    pixdata[x, y] = (pixdata[x-1, y][0],pixdata[x-1, y][1],pixdata[x-1, y][2],255)

    # for debugging
    img.save("temp.png")
    return pytesseract.image_to_string(img).replace(" ","").replace("\n","") # OCR

req = requests.get("http://challenge01.root-me.org/programmation/ch8/")
cookies = req.cookies.get_dict()
while True:
    if "img" not in req.content.decode():
        print("flag:",req.content.decode().split("flag est ")[1].replace("\n</p></p><br/></body></html>",""))
        break
    p = req.content.decode().split("<p>")[1].split("</p>")[0].replace(".<br>","")
    if p != "":
        print(f"[FAILED] {p}")
    imgstring = req.content.decode().split('<img')[1].split('>')[0].split('src="')[1].split('"')[0]
    imgstring = imgstring.split('base64,')[-1].strip()
    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)
    res = breaker(image, 0)
    if res == "":
        req = requests.get("http://challenge01.root-me.org/programmation/ch8/")
        cookies = req.cookies.get_dict()
        continue
    print(f"Test: {res}")
    req = requests.post("http://challenge01.root-me.org/programmation/ch8/", data={"cametu":res}, cookies=cookies)