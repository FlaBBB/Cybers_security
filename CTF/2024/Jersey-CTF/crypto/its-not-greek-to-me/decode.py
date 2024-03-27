def size_decryption(pf1):
    file_buff = 0
    for i in range(8):
        ch = pf1.read(1)
        bit_msg = ord(ch) & 1
        if bit_msg:
            file_buff = (file_buff << 1) | 1
        else:
            file_buff = file_buff << 1
    return file_buff


def string_decryption(pf1, size):
    file_buff = 0
    strng = ""
    for i in range(size * 8):
        ch = pf1.read(1)
        bit_msg = ord(ch) & 1
        if bit_msg:
            file_buff = (file_buff << 1) | 1
        else:
            file_buff = file_buff << 1
        if (i + 1) % 8 == 0:
            strng += chr(file_buff)
            file_buff = 0
    return strng


def secret_decryption(size_txt, pf1, pf2):
    file_buff = 0
    output = bytearray()
    for i in range(size_txt * 8):
        ch = pf1.read(1)
        bit_msg = ord(ch) & 1
        if bit_msg:
            file_buff = (file_buff << 1) | 1
        else:
            file_buff = file_buff << 1
        if (i + 1) % 8 == 0:
            pf2.write(bytes([file_buff]))
            output.append(file_buff)
            file_buff = 0


def decode(filename, output):
    with open(filename, "rb") as pf1:
        size1 = size_decryption(pf1)
        passwd_str = string_decryption(pf1, size1)

        passwd = input("Enter The Password: ")

        if passwd != passwd_str:
            print("\n*** Entered Wrong Password ***\n")
            return 0
        else:
            print("*** Password Accepted ***\n")

        size_txt = size_decryption(pf1)

        with open(output, "wb+") as pf2:
            secret_decryption(size_txt, pf1, pf2)
            print("The Secret Text is copied to:", output)


with open("JustSomeNormalPyramids.bmp", "rb") as f:
    size1 = size_decryption(f)
    passwd_str = string_decryption(f, size1)

    print(passwd_str.encode())
