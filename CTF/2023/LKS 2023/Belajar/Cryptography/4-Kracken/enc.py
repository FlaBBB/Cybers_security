from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32

key = '6b?dadcd478f76?0' # i think i lost my key :(
cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
msg = cipher.encrypt(pad(b'hello_world', BLOCK_SIZE))
print(msg)

#cipher=5ada0e30fd3c562e3db448f17bbd2169a7ba768c8492798698c3acc8446f1486
