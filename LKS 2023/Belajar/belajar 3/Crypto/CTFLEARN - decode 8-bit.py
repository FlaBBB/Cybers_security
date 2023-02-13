# print("41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D".encode('ascii'))
# bytes_list = [41, 42, 44, 54, 7B, 34, 34, 35, 43, 31, 31, 5F, 31]
# print(int.from_bytes(bytes.fromhex('7D'), byteorder='big', signed=True))
def decode_8_bit(encoded_str):
    import math
    decode_str = ""
    for a in range(math.ceil(len(encoded_str)/3)):
        offset = a*3
        decode_str += str(bytes.fromhex(encoded_str[offset:offset+2]))[2:-1]
    return decode_str


print(decode_8_bit("41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D"))
