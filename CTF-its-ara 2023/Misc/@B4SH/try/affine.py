
def mod_inv (num, mod):
    for x in range(0,mod + 1):
        if ((num*x)%mod == 1):
            return x
def brute(cipher, knowed_word = None):
    if not knowed_word == None:
        if len(knowed_word) > len(cipher):
            return 'error length'
    decipher = ""
    for i in range(0,26):
        if (i%2 != 0) and (i != 13):
            for j in range(0,26):
                inv = mod_inv(i,26)
                decipher_temp = ''
                for c in cipher:
                    v = ord(c)
                    if (v >= 65) and (v <= 90):
                        cip = ((v - 65 - j)*inv + 26)%26 + 65
                    elif (v >= 97) and (v <= 122):
                        cip = ((v - 97 - j)*inv + 26)%26 + 97
                    else:
                        cip = v
                    decipher_temp += chr(cip)
                if not knowed_word == None:
                    if knowed_word in decipher_temp:
                        decipher += decipher_temp+'\n'
                    continue
                decipher += decipher_temp+'\n'
    return decipher

cipher = "ZIZ2023{4mby0wb_gs0f9sg_gs4g_!g5_4_s4hs?}"

print(brute(cipher, 'ARA2023'))
