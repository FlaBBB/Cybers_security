from websockets.sync.client import connect
from io import BytesIO
from PIL import Image, ImageFilter

conn=connect("ws://172.86.96.174:8000/echo")
conn.send("0")
while 1:
    message = conn.recv()
    print(message)
    message2 = conn.recv()
    try:
        with BytesIO(message2) as f:
            img=Image.open(f).copy()
    except Exception as e:
        print(message2)
        break
    # img.show()
    imd=img.filter(ImageFilter.MinFilter()).filter(ImageFilter.MaxFilter()).getdata()
    # show imd
    print(imd.__class__)
    imd_cnt=len([i for i in imd if i!=imd[0]])
    conn.send(str(int(imd_cnt*100//img.size[0]//img.size[1])))