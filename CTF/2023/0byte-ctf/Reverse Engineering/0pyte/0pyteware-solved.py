from sys import argv, set_int_max_str_digits
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import md5
from random import randint, seed, choice
from string import ascii_letters
from base64 import b64encode, b64decode

set_int_max_str_digits(220000)

if __name__ == '__main__':
    def write_to_file(f, c): 
        return open(f'{f}.enc', 'wb').write(c)
    

    def encrypt(this_encoder_file_name: str, file_name: str) -> bytes:
        seed('0Byte')
        def xor_0x69(inp: list) -> bytes:
            res = bytearray()
            for i in inp:
                for j in bytes.fromhex(i):
                    res.append(j ^ 0x69)
            return bytes(res)
        
        iv = bytes.fromhex(md5(file_name.encode()).hexdigest())
        key = bytes.fromhex(md5(this_encoder_file_name.encode()).hexdigest())
        aes = AES.new(key, AES.MODE_CBC, iv)
        
        with open(file_name, 'rb') as FILE:
            padded_file = pad(FILE.read(), 16)
            enc = aes.encrypt(padded_file).hex().encode()

        x = []
        for i, e in enumerate(enc):
            if i % 2 == 0:
                x.append(e ^ randint(1, 255))
            else:
                x.append(e ^ ord(choice(ascii_letters)))

        y = []
        for i, j in enumerate(x):
            if i % 2 == 1:
                y.append(md5(chr(j).encode()).hexdigest())
            else:
                y.append('{:02X}'.format(j).lower())
        

        enc2 = xor_0x69(y)
        enc2 = b64encode(str(bytes_to_long(enc2)).encode())
        
        res = ""
        for i, z in enumerate(enc2):
            if i % 2 == 0:
                res += chr(z ^ 0x01)
            else:
                res += chr(z ^ 0x02)

        return res.encode()


    def brute_md5(hashes):
        for i in range(256):
            if md5(chr(i).encode()).hexdigest() == hashes:
                return i

    def decrypt(this_encoder_file_name: str, file_name: str) -> str:
        seed('0Byte')
        def dexor_0x69(inp: bytes) -> list:
            res = []
            for i, j in enumerate(inp):
                temp = '{:02x}'.format(j ^ 0x69)
                if i % 17 in [0, 1]:
                    res.append(temp)
                else:
                    res[(i // 17) + ((i // 17) + 1)] += temp
            return res
        
        with open(f"{file_name}.enc", 'rb') as FILE:
            cipher = FILE.read()
        
        enc2 = bytearray()
        for i, z in enumerate(cipher):
            if i % 2 == 0:
                enc2.append(z ^ 0x01)
            else:
                enc2.append(z ^ 0x02)

        enc2 = bytes(enc2)
        enc2 = long_to_bytes(int(b64decode(enc2).decode()))
        
        y = dexor_0x69(enc2)
        x = []
        for i, j in enumerate(y):
            if i % 2 == 1:
                x.append(brute_md5(j))
            else:
                x.append(int(j, 16))
                
        enc = ""
        for i, j in enumerate(x):
            if i % 2 == 0:
                enc += chr(j ^ randint(1, 255))
            else:
                enc += chr(j ^ ord(choice(ascii_letters)))
        
        iv = bytes.fromhex(md5(file_name.encode()).hexdigest())
        key = bytes.fromhex(md5(this_encoder_file_name.encode()).hexdigest())
        aes = AES.new(key, AES.MODE_CBC, iv)
        
        res = aes.decrypt(bytes.fromhex(enc))
        res = unpad(res, 16)
        
        return res
        
    # argv_1 = "flag.png"
    argv_1 = "flag.png"
    # write_to_file(argv_1, encrypt(argv[0], argv_1))
    # encrypt("test", argv_1)
    # print(argv[0])
    argv_0 = "0pyteware.py"
    res = decrypt(argv_0, argv_1)
    print(res)
    
    with open(argv_1, 'wb') as FILE:
        FILE.write(res)
