from base64 import b64decode
from io import BytesIO

import requests
from latex2sympy2 import latex2sympy
from PIL import Image
from pix2tex.cli import LatexOCR

model_latexOCR = LatexOCR()

url = "https://peterparker.q.2024.ugractf.ru/uxnor4rbzpscdc2z/"


def base64_to_img(buff: str):
    # print(buff.split("data:image/png;base64,")[1])
    return Image.open(BytesIO(b64decode(buff.split("data:image/png;base64,")[1])))


def img_to_latex(img: Image):
    return model_latexOCR(img)


def get_state():
    response = requests.get(url + "state")
    return response.json()


def click(data: dict = {}):
    response = requests.post(url + "click", json=data)
    return response.json()


data = get_state()
counter = data["counter"]
print(data)
while counter > 0:
    data = click()
    counter = data["counter"]
    if not data["need_captcha"]:
        continue
    print(f"Trying to solve captcha {counter} left")
    image = base64_to_img(data["picture"])
    latex = img_to_latex(image)
    try:
        sympy_expr = latex2sympy(latex.replace("\ ", "").replace(" ", ""))
    except Exception as e:
        print(f"Error: {e}")
        continue
    result = round(sympy_expr.evalf(), 3)
    data = click({"captcha_response": float(result)})
    if data.get("retry_captcha", False):
        print(f"Result: {result} is incorrect")
    else:
        print(f"Result: {result} is correct")


print(data["flag"])
