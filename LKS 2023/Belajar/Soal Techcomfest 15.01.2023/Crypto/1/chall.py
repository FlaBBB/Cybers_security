
SECRET_WORD = "nino"


def hash_code(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return h


def hash_code1(s):
    h = 0
    for c in s:
        h = (31 * h + ord(c))
    return h


def findAllCombinations(A, k, subarrays, out=""):

    # invalid input
    if len(A) == 0 or k > len(A):
        return

    # base case: combination size is `k`
    if k == 0:
        subarrays.add(out)
        return

    # start from the next index till the last index
    for j in range(len(A)):
        # add current element `A[j]` to the solution and recur for next index
        # `j+1` with one less element `k-1`
        findAllCombinations(A, k - 1, subarrays, out + A[j])


def brute(result):
    brute_list = (
        # " ",
        # "!",
        # "\"",
        # "#",
        # "$",
        # "%",
        # "&",
        # "'",
        # "(",
        # ")",
        # "*",
        # "+",
        # ",",
        # "-",
        # ".",
        # "/",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        # ":",
        # ";",
        # "<",
        # "=",
        # ">",
        # "?",
        # "@",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        # "[",
        # "\\",
        # "]",
        # "^",
        # "_",
        # "`",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        # "{",
        # "|",
        # "}",
        # "~"
    )

    len = 1
    hasil = []
    jumlah_hasil = 0
    while True:

        subarrays = set()
        findAllCombinations(brute_list, len, subarrays)
        for sub in subarrays:
            print(sub)
            h = hash_code(sub)
            if h == result:
                hasil.append(sub)
                print(hasil)
                jumlah_hasil += 1
                if jumlah_hasil >= 2:
                    return hasil
        len += 1


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


# if __name__ == "__main__":
#     main()

# print(hash_code("nino"))
# print(hash_code1("aimardcr"))
# print(4298348731)

# target = 4298348731

print(brute(3381436))
# print(brute(3591))

# print(hash_code("oP"))
# print(hash_code("pw"))
