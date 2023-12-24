import os

key = os.urandom(8)
sbox = [98, 56, 7, 192, 121, 149, 107, 246, 120, 132, 191, 152, 229, 238, 94, 106, 176, 170, 161, 253, 145, 181, 237, 211, 219, 250, 131, 190, 158, 24, 126, 32, 79, 212, 244, 53, 60, 183, 83, 128, 162, 137, 15, 148, 50, 51, 166, 92, 171, 88, 44, 242, 69, 91, 101, 103, 175, 3, 82, 40, 245, 110, 34, 143, 248, 35, 109, 115, 227, 47, 140, 122, 193, 59, 39, 243, 208, 55, 165, 213, 224, 231, 96, 185, 151, 100, 105, 12, 66, 42, 160, 214, 205, 189, 130, 5, 147, 20, 236, 85, 142, 194, 2, 228, 124, 215, 14, 26, 240, 223, 154, 203, 54, 25, 141, 200, 8, 111, 177, 0, 75, 73, 204, 80, 230, 58, 112, 10, 52, 157, 116, 41, 4, 217, 18, 9, 174, 27, 226, 163, 36, 13, 167, 72, 241, 21, 186, 30, 87, 221, 168, 89, 239, 29, 178, 179, 249, 45, 195, 57, 95, 22, 180, 153, 129, 108, 201, 202, 63, 68, 64, 135, 207, 156, 133, 220, 11, 71, 6, 233, 232, 119, 173, 90, 102, 117, 136, 86, 247, 76, 234, 164, 172, 184, 78, 225, 125, 199, 46, 210, 216, 123, 31, 235, 182, 251, 38, 206, 139, 197, 159, 127, 150, 61, 16, 19, 28, 198, 93, 77, 49, 169, 1, 114, 134, 187, 188, 67, 113, 74, 218, 104, 254, 65, 196, 155, 144, 209, 37, 81, 70, 48, 43, 84, 138, 62, 17, 23, 222, 118, 146, 33, 99, 252, 97]

def encrypt(s, key):
    S = list(range(0xff))
    j = 0
    out = []

    for i in range(0xff):
        j = (j + S[i] + key[i % len(key)])
        j %= 0xff
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for char in s:
        i += 1
        i %= 0xff
        j += S[i]
        j %= 0xff
        S[i], S[j] = S[j], S[i]
        out.append(chr(sbox[ord(char) ^ S[(S[i] + S[j]) % 0xff]]))

    return ''.join(out)

def main():
    flag = open('flag.txt', 'r').read()
    while True:
        print("1. Get Encrypted Flag")
        print("2. Encrypt")
        print("3. Exit")
        try:
            choice = int(input("> "))
            if choice == 1:
                print(encrypt(flag, key).encode('latin1').hex())
            elif choice == 2:
                s = input("Enter string to encrypt: ")
                print(encrypt(s, key).encode('latin1').hex())
            elif choice == 3:
                break
            else:
                print("Invalid choice")
        except:
            print('Something went wrong...')

if __name__ == '__main__':
    main()