import binascii
import string

with open("file.enc", 'rb') as FILE:
    buffer = FILE.read()

# for i in range(0x100):
#     for b in buffer:
#         res = chr(b ^ i)
#         if res not in string.printable:
#             break
#         print(res, end='')
#     print()

# print(len(buffer))
# for b in buffer:
#     print(b)

print(binascii.hexlify(buffer))