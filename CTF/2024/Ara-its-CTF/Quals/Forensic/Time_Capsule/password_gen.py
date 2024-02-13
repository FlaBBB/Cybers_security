import string

pass_element = [
    [i for i in range(1, 13)],
    ["kAor1", "s3nKu", "sTev3", "Lev1", "L1Ly"],
    ['*', '#', '!', '%', '&', '+'],
    [i for i in range(10)],
    [i for i in string.ascii_uppercase],
    ['*', '#', '!', '%', '&', '+']
]

# create the generator function to generate the password from element, recursively using yield
def gen_pass(pass_element):
    if len(pass_element) == 1:
        for i in pass_element[0]:
            yield i
    else:
        for i in pass_element[0]:
            for j in gen_pass(pass_element[1:]):
                yield str(i) + str(j)

possibilities = 1
for element in pass_element:
    possibilities *= len(element)

print("Total possibilities: ", possibilities)
with open("password.txt", "w") as f:
    for i in gen_pass(pass_element):
        f.write(i + "\n")