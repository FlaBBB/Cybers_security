from base64 import *

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

pt = "this is a top secret: 3452617894185123628579729857329"

pt = pad(pt.encode(), 8)

cp = DES.new(b"00001111", DES.MODE_ECB)
ct = cp.encrypt(pt)

cp = DES.new(b"11110000", DES.MODE_ECB)
ct = cp.encrypt(ct)

cp = DES.new(b"11111111", DES.MODE_ECB)
ct = cp.encrypt(ct)

cp = DES.new(b"00000000", DES.MODE_ECB)
ct = cp.encrypt(ct)

cp = DES.new(b"10101010", DES.MODE_ECB)
ct = cp.encrypt(ct)

cp = DES.new(b"01010101", DES.MODE_ECB)
ct = cp.encrypt(ct)

cp = DES.new(b"01010000", DES.MODE_ECB)
ct = cp.encrypt(ct)

# ----------------------------------------------

cp = DES.new(b"00001111", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"10101010", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"11111111", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"01010101", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"11110000", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"01010000", DES.MODE_ECB)
ct = cp.decrypt(ct)

cp = DES.new(b"00000000", DES.MODE_ECB)
pt = cp.decrypt(ct)

print(pt)
