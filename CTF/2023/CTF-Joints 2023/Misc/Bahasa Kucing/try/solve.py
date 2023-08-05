cat = open("from_c4t").read().split(" ")
akehe = dict()

for c in cat:
    if c == "":
        continue
    if c not in akehe:
        akehe[c] = 1
    else:
        akehe[c] += 1

akehe = dict(sorted(akehe.items(), key=lambda item: item[1]))
akehe = dict(reversed(list(akehe.items())))
print(akehe)

DICTIONARY = {
    "meaw" : "a",
    "meeaw" : "N",
    "mrr" : "E"
}
text = ""
for c in cat:
    if c in DICTIONARY:
        c = DICTIONARY[c]
    else:
        c = "X"
    text+=c
    
print(text)