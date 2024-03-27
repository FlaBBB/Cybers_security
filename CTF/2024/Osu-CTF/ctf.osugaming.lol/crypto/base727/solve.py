

encoded_string = open("out.txt").read()
encoded_string = bytes.fromhex(encoded_string).decode()


def decode_base_727(string):
    base = 727
    decoded_value = 0

    for char in string:
        decoded_value = decoded_value * base + ord(char)

    decoded_string = ""
    while decoded_value > 0:
        decoded_string = chr(decoded_value % 256) + decoded_string
        decoded_value //= 256

    return decoded_string


flag = decode_base_727(encoded_string)

print(flag)
