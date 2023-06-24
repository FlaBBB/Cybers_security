import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def b16_decode(cipher):
    plain = ""
    temp = ""
    for c in cipher:
        if temp == "":
            temp = "{0:04b}".format([i for i in range(len(ALPHABET)) if ALPHABET[i] == c][0])
            continue
        plain += chr(int(temp + "{0:04b}".format([i for i in range(len(ALPHABET)) if ALPHABET[i] == c][0]), base=2))
        temp = ""
    return plain

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

def unsift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 - t2) % len(ALPHABET)]

# flag = "redacted"
# key = "redacted"
# assert all([k in ALPHABET for k in key])
# assert len(key) == 1

# b16 = b16_encode(flag)
# enc = ""
# for i, c in enumerate(b16):
# 	enc += shift(c, key[i % len(key)])
# print(enc)

def decrypt(cipher):
    for key in ALPHABET:
        plain = ""
        for c in cipher:
            plain += unsift(c,key)
        try:
            plain = b16_decode(plain).encode()
            print(f"{key} =",plain)
        except:
            continue
cipher = 'lkmjkemjmkiekeijiiigljlhilihliikiliginliljimiklligljiflhiniiiniiihlhilimlhijil'
decrypt(cipher)
