import re
s = ('2', '_', 'e', 'n', 'u', 's', '3', '3', 'n', 'n', 'T', 'C', '_', '_', '2', '0', 'r', 't', 'g', '1', '0', '_', 'J', 'h', 's', 'w', '{', '4', 'e', 'u', '3', 'y', '}', '_', '3', 'F', 'o', 'd', '_', 'e', 'j', 'i', 't')
s = s[::-1]
r = open("res.pyasm").read().split("\n\n")
for x in r[3:]:
    x = re.search(f"LOAD_CONST +\d+ \(\d+\)", x).group()[:-1].split("(")[1]
    print(s[int(x)], end="")