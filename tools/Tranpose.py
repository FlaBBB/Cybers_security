cipher = "heTfl g as iicpCTo{7F4NRP051N5_16_35P3X51N3_V6E5926A}4"


tranpose_offset = 3
def decrypt(cipher, tranpose_offset):
    res = ""
    for i in range(0, len(cipher), tranpose_offset):
        res += cipher[i + tranpose_offset - 1] + cipher[i:i + tranpose_offset - 1]
    return res

print(decrypt(cipher, tranpose_offset))