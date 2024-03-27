def decryptor(file):
    cipher = open(file, "rb").read()
    plain = bytearray(4056)
    cipher = [cipher[i : i + 8] for i in range(0, len(cipher), 8)]
    for i in range(255):
        size = int.from_bytes(cipher.pop(0), "little")
        for _ in range(size):
            offset = int.from_bytes(cipher.pop(0), "little")
            plain[offset] = i

    return bytes(plain).strip(b"\x00")


print(decryptor("message.txt.cz").decode())
