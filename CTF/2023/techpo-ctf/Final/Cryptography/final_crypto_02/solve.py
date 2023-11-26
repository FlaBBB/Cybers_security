def decrypt(message, key):
    decrypted_text = bytearray()
    for char in message:
        decrypted_text.append(ord(char) - key)
    return decrypted_text

def main():
    with open("cipher.txt", "r", encoding="utf-8") as f:
        ciphertext = f.read()

    for key in range(256):
        plaintext = decrypt(ciphertext, key)
        print(key, plaintext)

if __name__ == "__main__":
    main()