def main():
    s1 = list("Z\x15qYU'\x0Eu")
    v10 = [0x39727E370854130A, 0x4F721D155539727E, 0x5C552D5857311246]
    s = input("Enter the key: ")

    if len(s) == 7:
        for i in range(len(s1)):
            s1[i] = chr(ord(s[i % len(s)]) ^ ord(s1[i]))

        if "".join(s1).startswith("TCF2024"):
            print("Correct key!")
            return 0
        else:
            print("Invalid key")
            return 1
    else:
        print("Invalid key length")
        return 1


if __name__ == "__main__":
    main()
