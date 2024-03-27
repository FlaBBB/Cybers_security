def create_topping(curr, idx):
    temp = 0
    num = 1 << 1
    while curr:
        remainder = curr % idx
        if remainder:
            temp = temp * 10 + remainder
            curr = curr - remainder
        else:
            num |= 1
            curr //= idx
        num <<= 1
    temp <<= 1
    temp |= 1
    return temp, num | 1


def create_base(not_remainder):
    num = 0
    for _ in range(30):
        if not_remainder:
            num |= not_remainder & 1
            not_remainder >>= 1
        num <<= 1
    return num


def create(curr, idx):
    not_remainder, topping = create_topping(curr, idx)
    base = create_base(not_remainder)
    return base | topping


def check_validity(num):
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def extra_security(encryption):
    for i, num in enumerate(encryption):
        idx = i + 2
        if check_validity(idx):
            encryption[i] = ~num


def encode(encryption, data, key):
    for i, char in enumerate(data):
        curr = ord(char)
        idx = (i % 8) + 2
        num = create(curr, idx)
        encryption.append(num)


def apply_key(encryption, key):
    for i, char in enumerate(key):
        curr = ord(char)
        cnt = bin(curr).count("1")
        curr <<= i + 10
        for _ in range(cnt):
            curr = (curr << 1) ^ 1
        k = len(encryption)
        for j in range(k):
            encryption[j] ^= curr


def write_to_file(encryption):
    with open("Encrypted.txt", "w") as outfile:
        data = " ".join(map(str, encryption))
        outfile.write(data)


def main():
    with open("Flag.txt") as file:
        data = file.read().strip()
    encryption = []
    key = "VishwaCTF"
    encode(encryption, data, key)
    apply_key(encryption, key)
    extra_security(encryption)
    write_to_file(encryption)


if __name__ == "__main__":
    main()
