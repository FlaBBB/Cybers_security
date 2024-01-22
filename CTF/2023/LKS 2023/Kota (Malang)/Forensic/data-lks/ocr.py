import json
import sys

import requests
from PIL import Image


def crop_image(input_image, output_image, start_x, start_y, width, height):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping, width to crop, height to crop"""
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image + ".png")


def ocr_space_file(
    filename, overlay=False, api_key="helloworld", language="eng", OCREngine=2
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
        "OCREngine": OCREngine,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key="helloworld", language="eng"):
    """OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "url": url,
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    r = requests.post(
        "https://api.ocr.space/parse/image",
        data=payload,
    )
    return r.content.decode()


# Use examples:
# test_file = ocr_space_file(filename='example_image.png', language='pol')
# test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')

stringa = ""
for i in range(131):
    # print("gambar ke " + str(i))
    FilePath = "data\\img" + str(i) + ".png"
    Engine = 2
    crop_image(
        FilePath, "data\\img" + str(i) + "-cropped", 200 - 136, 200 - 120, 95, 80
    )
    ocr_res = ""
    while len(ocr_res) < 2:
        if Engine == 6:
            print(" -- Error")
            break
        ocr_res = json.loads(
            ocr_space_file(
                "data\\img" + str(i) + "-cropped.png",
                api_key="K82695434588957",
                OCREngine=Engine,
            )
        )["ParsedResults"][0]["ParsedText"]
        Engine = +1
        print("hasil ocr gambar img" + str(i) + ": " + ocr_res, end="")
    print("")
    stringa += ocr_res

f = open("string_ocr_dari_depan.txt", "w")
f.write(stringa)
f.close()
