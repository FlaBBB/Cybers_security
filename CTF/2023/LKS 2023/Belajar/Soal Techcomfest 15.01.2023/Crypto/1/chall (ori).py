#!/usr/bin/python

SECRET_WORD = "nino"

def hash_code(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return h

def main():
    with open("flag.txt", "r") as f:
        flag = f.read()

    print("Do you know the secret word?")
    s = input(">> ")

    if s != SECRET_WORD:
        if hash_code(s) == hash_code(SECRET_WORD):
            print("Noice!")
            print("Here's your flag: " + flag)
        else:
            print("Hmmm, are you sure about that?")
    else:
        print("Oopsie, you can't do that!")


if __name__ == "__main__":
    main()