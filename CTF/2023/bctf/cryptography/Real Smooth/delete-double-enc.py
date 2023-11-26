database = open("database.txt", "r").readlines()
res = []
for d in database:
    if d not in res:
        res.append(d)

with open("database.txt", "w") as f:
    for r in res:
        f.write(r)