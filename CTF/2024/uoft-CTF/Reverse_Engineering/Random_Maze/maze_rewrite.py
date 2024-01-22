path = b""
flag = b"ON#X~o8&"
sums = [0xCE, 0xA1, 0xAE, 0xAD, 0x64, 0x9F, 0xD5]


def oops():
    print("woopsie! got something wrong there!")
    exit(69)


def check_prime(n):
    if n <= 1:
        return False
    for i in range(2, n // 2):
        if n % i == 0:
            return False
    return True


def transverse(i):
    global flag, path
    flag = flag[:i] + bytes([flag[i] ^ path[i]]) + flag[i + 1 :]
    if i != 0:
        if flag[i] + flag[i - 1] != sums[i - 1]:
            oops()
    else:
        result = check_prime(flag[0])
        if not result:
            oops()


def main():
    global path
    print("can you solve the maze? :3")
    try:
        path = bytes.fromhex(input("choose ur path >> ").strip())[::-1]
    except ValueError:
        oops()
    print("running your path! hope this works: ", end="")

    for i in range(8):
        if (
            path[i] & 3 == 0
            or path[i] == 3 * (path[i] // 3)
            or path[i] > 100
            or path[i] <= 19
        ):
            oops()
        else:
            transverse(i)
    print(f"uoftctf{{{flag.decode()}}}")


main()
