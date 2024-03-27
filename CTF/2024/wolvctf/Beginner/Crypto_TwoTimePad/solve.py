from Crypto.Random import get_random_bytes, random

BLOCK_SIZE = 16

with open("./eWolverine.bmp", "rb") as f:
    wolverine = f.read()
with open("./eFlag.bmp", "rb") as f:
    flag = f.read()

f = open("mix.bmp", "wb")

f.write(flag[:55])

for i in range(55, len(flag), BLOCK_SIZE):
    f.write(
        bytes(
            a ^ b
            for a, b in zip(flag[i : i + BLOCK_SIZE], wolverine[i : i + BLOCK_SIZE])
        )
    )
