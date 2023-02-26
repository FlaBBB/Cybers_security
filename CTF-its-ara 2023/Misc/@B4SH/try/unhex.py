from pwn import *
hex= '5A495A323032337B346D62793077625F677330663973675F677334675F2167355F345F733468733F7D'

print(binascii.a2b_hex("%s" % (hex.strip())).decode("ASCII").replace(';', '\n- '))
