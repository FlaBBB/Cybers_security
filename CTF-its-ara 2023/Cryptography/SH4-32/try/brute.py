import hashlib
import sys
from pwn import binascii

def combine(a,b, separator = False):
    ret = []
    for x in a:
        for y in b:
            if separator:
                ret.append(x+"_"+y)
            else:
                ret.append(x+y)
    return ret


d_raw = open("Dictionary.txt").readlines()
DICTIONARY = []
for d in d_raw:
    DICTIONARY.append(d.strip())

cipher = "9be9f4182c157b8d77f97d3b20f68ed6b8533175831837c761e759c44f6feeb8"
format = "ARA2023{"
list_brute = []
breaks = False
loop = 1
is_separator = True
is_with_format = True
print('with format & separator:')
while True:
    print(loop)
    if is_with_format:
        if list_brute == []:
            list_brute = combine(format,DICTIONARY)
        else:
            list_brute = combine(list_brute,DICTIONARY, is_separator)
    else:
        if list_brute == []:
            list_brute = combine([''],DICTIONARY)
        else:
            list_brute = combine(list_brute,DICTIONARY, is_separator)

    for t in list_brute:
        if is_with_format:
            t = t+"}"
        temp_hash = []
        temp_hash.append(hashlib.sha256((t).encode()).hexdigest())
        temp_hash.append(hashlib.sha384((t).encode()).hexdigest())
        temp_hash.append(hashlib.sha224((t).encode()).hexdigest())
        temp_hash.append(hashlib.sha512((t).encode()).hexdigest())
        if cipher in temp_hash:
            print("result: "+binascii.unhexlify(t).decode())
            breaks = True
            break
    if breaks:
        break
    if loop >= 2:
        if is_separator == True:
            print("now with out separator")
            is_separator = False
            list_brute = []
            loop == 1
            continue
        else:
            if is_with_format == True:
                print("now with out format & with separator")
                is_with_format = False
                is_separator = True
                list_brute = []
                loop == 1
                continue
            else:
                sys.exit("this not work")
    else:
        loop += 1
