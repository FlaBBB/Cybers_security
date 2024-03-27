import random
import string
import time

flag_dict = (string.ascii_letters + string.digits + "{}_").encode()


def check(s: bytes):
    for x in s:
        if x not in flag_dict:
            return False
    return True


cipher = [192, 123, 40, 205, 152, 229, 188, 64, 42, 166, 126, 125, 13, 187, 91]

start = time.strptime("31 December 2023 00.00 GMT-11:00", "%d %B %Y %H.%M %Z%z")
end = time.strptime("2 January 2024 23.59 GMT+11:00", "%d %B %Y %H.%M %Z%z")
seed_start = int(time.mktime(start))
seed_end = int(time.mktime(end))

print(f"Start seed: {seed_start}")
print(f"End seed: {seed_end}")
for seed in range(seed_start, seed_end):
    res = b""
    for i in range(len(cipher)):
        random.seed(i + seed)
        res += bytes([cipher[i] ^ random.getrandbits(8)])
        seed += random.randint(1, 60)
    if check(res):
        print(res)
