from pwn import *
import string
from random import shuffle

def shuffle_word(word):
    word = list(word)
    shuffle(word)
    return ''.join(word)

DICT = string.ascii_letters + string.digits + string.punctuation

HOST = 'mercury.picoctf.net'
PORT = 58251

io = connect(HOST, PORT)

flag = io.recvuntil(b'I will encrypt whatever you give me:').split(b'\n')[0].split(b' ')[-1].decode()

chars = []
r_flag = 'picoCTF{bad_1d3a5_1314164}'
if len(r_flag) != len(chars):
    chars = []
    for i in range(len(r_flag)):
        io.sendline(r_flag[:i + 1].encode())
        res = io.recvuntil(b'I will encrypt whatever you give me:').split(b'\n')[0].split(b' ')[-1].decode()
        for c in chars:
            assert c in res
            res = res.replace(c, '').strip()
        assert res in flag
        chars.append(res)
        flag = flag.replace(res, '')

while flag:
    for i in DICT:
        io.sendline((r_flag + i).encode())
        res = io.recvuntil(b'I will encrypt whatever you give me:').split(b'\n')[0].split(b' ')[-1].decode()
        for c in shuffle_word(chars):
            assert c in res
            res = res.replace(c, '').strip()
        if res in flag:
            chars.append(res)
            r_flag += i
            flag = flag.replace(res, '')
            break
    assert (res in flag) or (res in chars)
    print(r_flag, chars)

print("Flag:", r_flag)