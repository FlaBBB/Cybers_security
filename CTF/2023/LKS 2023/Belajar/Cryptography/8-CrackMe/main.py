import random
import string
from base64 import *

def encrypt(plain,key):
  res = ""
  for i in plain:
    res += chr(ord(i) ^ ord(key))
  return b64encode(res)

if __name__ == "__main__":
    test = "hello world!"
    randkey = random.choice(string.ascii_letters)
    enc = encrypt(test,randkey)
    print("%s"%(enc))