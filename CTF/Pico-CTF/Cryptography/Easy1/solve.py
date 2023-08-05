def unpad(cipher, key):
    plain = ""
    for i, c in enumerate(cipher):
        plain += chr((((ord(c) - ord('A')) - ord(key[i%len(key)]) - ord('A')) % 26) + ord('A'))
    return plain

print(unpad("UFJKXQZQUNB", "SOLVECRYPTO"))