# 1:10:d0:10:42:41:34:20:b5:40:03:30:91:c5:e1:e3:d2:a2:72:d1:61:d0:10:e3:a0:43:c1:01:10:b1:b1:b0:b1:40:9
# snub_wrestle

from pwn import xor
import string

dictionary = (string.ascii_letters + string.digits + string.punctuation + " ").encode("latin-1")

cipher = "1:10:d0:10:42:41:34:20:b5:40:03:30:91:c5:e1:e3:d2:a2:72:d1:61:d0:10:e3:a0:43:c1:01:10:b1:b1:b0:b1:40:9".split(":")

class logger:
    last_long = 0
    def __print(self, message):
        message = str(message)
        print(message, end="")
        self.last_long = len(message)
    
    def print_log_replace(self, message):
        self.__print(" " * abs(self.last_long - len(message)) + "\r" + message)

    def print(self, message):
        self.__print(message + "\n")

def combine(a, b):
    for x in a:
        for y in b:
            yield x + y

def checking_isprintable(a:bytearray or bytes, dictionary:bytes):
    for i in a:
        if i not in dictionary:
            return False
    return True


# def getting_key(cipher, key = b"", dictionary = dictionary):
#     res = []
#     log = logger()
#     for d in dictionary:
#         is_seems_valid = False
#         t_key = key + d.to_bytes()
#         for i in range(0, len(cipher) - len(key)):
#             temp = bytearray()
#             for j, pk in zip(cipher[i:], t_key):
#                 temp.append(int(j, 16) ^ pk)
#             if checking_isprintable(temp, dictionary):
#                 is_seems_valid = True
#                 break
#         if is_seems_valid:
#             log.print_log_replace(t_key)
#             if len(t_key) == len(cipher):
#                 return t_key
#             nkey = getting_key(cipher, t_key)
#             if nkey != []:
#                 res += nkey
#     return res

# print(getting_key(cipher, b""))

def getting_key(cipher, dictionary = dictionary):
    map_key = dict()
    for i, c in enumerate(cipher):
        map_key[i] = []
        for d in dictionary:
            temp = (int(c, 16) ^ d).to_bytes()
            if checking_isprintable(temp, dictionary):
                map_key[i].append(chr(d))
    res = [""]
    for i in map_key:
        res = combine(res, map_key[i])

    return res

log = logger()
key = getting_key(cipher)
for i in key:
    log.print(i)