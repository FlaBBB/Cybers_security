from pwn import binascii
import string

cipher = binascii.unhexlify('001300737173723a70321e3971331e352975351e247574387e3c').decode()

def combine(a, b):
    ret = []
    for x in a:
        for y in b:
            ret.append(x + y)
    return ret


brute = string.printable
knowed_text = "ARA2023{"
brute_list = ['']
is_breaks = False
loops = 1
while True:
    print("length key: " + str(loops))
    brute_list = combine(brute_list, brute)
    for b in brute_list:
        text = ''
        for t in cipher:
            for x in b:
                text += chr(ord(t) ^ ord(x))
        if knowed_text in text:
            is_breaks = True
            print("result: " + text)
            break
    if is_breaks:
        break
    loops += 1
