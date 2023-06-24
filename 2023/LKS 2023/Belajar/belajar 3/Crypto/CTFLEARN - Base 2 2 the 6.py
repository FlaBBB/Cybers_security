from base64 import b64decode
encoded = "Q1RGe0ZsYWdneVdhZ2d5UmFnZ3l9"
print(b64decode(encoded.encode("utf-8")).decode("utf-8"))
