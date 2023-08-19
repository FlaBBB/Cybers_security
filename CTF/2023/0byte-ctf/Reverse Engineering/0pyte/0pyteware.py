#!/usr/bin/python3

from sys import argv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long
from hashlib import md5
from random import randint, seed, choice
from string import ascii_letters
from base64 import b64encode

if __name__ == '__main__':
	seed('0Byte')
	w = lambda f, c: open(f'{f}.enc', 'wb').write(c)
	e = lambda a,b: ''.join([chr(z^0x01) if zzz % 2 == 0 else chr(z^0x02) for zzz,z in enumerate(b64encode(str(bytes_to_long(bytes.fromhex(''.join([xxxxx for xxxxx in map(lambda _: ''.join(['{:02X}'.format(yy^0x69) for yy in bytes.fromhex(_)]), [md5(chr(lr).encode()).hexdigest() if ll % 2 == 1 else '{:02X}'.format(lr).lower() for ll,lr in enumerate([iii ^ randint(1, 255) if jjj % 2 == 0 else iii^ord(choice(ascii_letters)) for jjj,iii in enumerate(AES.new(bytes.fromhex(md5(a.encode()).hexdigest()), AES.MODE_CBC, bytes.fromhex(md5(b.encode()).hexdigest())).encrypt(pad(open(b, 'rb').read(), 16)).hex().encode())])])])))).encode()))]).encode()
	w(argv[1], e(argv[0], argv[1]))
