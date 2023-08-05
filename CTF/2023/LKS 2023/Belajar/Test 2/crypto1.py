import codecs
sampleString = "flag"

inpString = sampleString

xorKey = 'P'

length = len(inpString)
print("Encrypted String: ", end="")

for i in range(length):
    inpString = (inpString[:i] + chr(ord(inpString[i]) ^ ord(xorKey)) + inpString[i + 1:])
    print(inpString[i], end="")
s = inpString.encode('utf-8')

# cipher=b'\x1c\x1b\xO3\x1d\x1b+\x125<1:1"p\xO351>:1>7p\x181)1$-'
