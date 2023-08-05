import codecs
sampleString = "flag"

def encrypt(sampleString):
    inpString = sampleString

    xorKey = 'P'

    length = len(inpString)
    # print("Encrypted String: ", end="")

    for i in range(length):
        # print(inpString)
        inpString = (inpString[:i] + chr(ord(inpString[i]) ^ ord(xorKey)) + inpString[i + 1:])
        # print(inpString[i], end="")
    # print(inpString)
    s = inpString.encode('utf-8')
    print("")
    print(s)

encrypt("LKS30SMK{Belajar Seanjang Hayat}")

# b'41=1"p\'92%#5>5>71>5>45<?;1>9=5'
# b'41=1"\'92%#5>5>71>5>45<?;1>9=5'
# b'41=1"p\'92%p#5>5>71>5p>45<?;p1>9=5'
# b'\x0b\x0e\x02\x0e\x1dO\x18\x06\r\x1aO\x1c\n\x01\n\x01\x08\x0e\x01\nO\x01\x0b\n\x03\x00\x04O\x0e\x01\x06\x02\n'

# cipher=b'\x1c\x1b\xO3\x1d\x1b+\x125<1:1"p\xO351>:1>7p\x181)1$-'

from base64 import b64encode
from base64 import b64decode

def decrypt(cipher):
    cipher = cipher[2:-1]

    xorKey = 'P'

    length = len(cipher)

    for i in range(length):
        # print(cipher)
        cipher = (cipher[:i] + chr(ord(cipher[i]) ^ ord(xorKey)) + cipher[i + 1:])
        # print(cipher[i], end="")
    s = cipher
    # print("")
    print("Decrypted String: ", end="")
    print(s)


# def decrypt(cipher):
#     cipher = codecs.decode(cipher[2:-1].encode(), "utf-8")
#     print(cipher)

# cipher="b'\x1c\x1b\x03c`\x03\x1d\x1b+\x125<1:1\"p\x0351>:1>7p\x181)1$-'"
cipher = "b'\x1c\x1b\x03\x1d\x1b+\x125<1:1\"p\x0351>:1>7p\x181)1$-'"
# cipher = "b'6\"%9$p\\x0451'"

decrypt(cipher)