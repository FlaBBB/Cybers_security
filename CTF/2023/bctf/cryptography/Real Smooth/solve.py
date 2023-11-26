from Crypto.Util.number import *
from pwn import xor

c1 = bytes.fromhex("c1229ab7b6350824f2dc11e8510fc249ad48") # take cipher that seems to be the same length
c2 = bytes.fromhex("d52b94abaa350824f2dc11e8510fc249ad48")

attack = xor(c1, c2)
long_null = attack.count(b"\x00")

c_m1 = b"\xff" * (18 - long_null) + b"\x00" * long_null # gen new m1 with known long null
partial_key = xor(c_m1, c1) # get partial key from m1 and c1

c3 = bytes.fromhex("c43c9cb4b225636abd8e5ea6104386068748") # take another cipher has longer length
m3 = xor(c3, partial_key)
print(f"{partial_key = }")
print(f"{m3 = }") # analyze m3 to predict the actual message of m3

# ===========================================================================

m3 = b"CRISTIANORONALDO*\x00" # from analyze m3 (the partial m3 b'\xfa\xe1\xf9\xfc\xfb\x10kNORONALDO*\x00')
key = b""
for m, c in zip(m3, c3):
    if m == ord("?"):
        key += b"\xff"
        continue
    key += (m ^ c).to_bytes()

print(f"{key = }")

# ===========================================================================

database = open("database.txt", "r").readlines()
database = list(map(lambda x: bytes.fromhex(x.strip()), database))

def checking(key:bytes, is_printable:bool = False, searching:bytes = None):
    if searching is None:
        print("+" + "-" * 32 + "CHECKING" + "-" * 32 + "+")
    for i in database:
        res = xor(i, key)
        if is_printable:
            res = res.strip(b"\x00")
        if searching is not None and searching in res: 
            return (i, res)
        if searching is None and (not is_printable or not res.decode("latin-1").isprintable()):
            print(res)
    if searching is None:
        print("+" + "-" * 32 + "CHECKING" + "-" * 32 + "+")

def replacing_keys(initial_message, replaced_message, key):
    cipher, full_message = checking(key, False, initial_message)
    replaced_message += full_message[len(replaced_message):]
    print(f"{replaced_message = }")
    print(f"{full_message = }")
    key = xor(cipher, replaced_message)
    return key

# checking(key)

searching = b"LOVEALWAYS*"
replace = b"lovealways\n".ljust(18)

key = replacing_keys(searching, replace, key)
checking(key)

# ===========================================================================