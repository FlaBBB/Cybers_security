def encrypt(message, key):
    encrypted_text = ""
    for char in message:
        encrypted_text += chr(ord(char) + key)
    return encrypted_text

def main():
    message = "flag{ini_contoh_flag}"
    key = 42

    ciphertext = encrypt(message, key)
    with open("cipher-test.txt", "w") as f:
        f.write(ciphertext)

if __name__ == "__main__":
    main()
