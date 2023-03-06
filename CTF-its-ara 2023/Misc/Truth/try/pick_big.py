import string

ALLOWED = string.ascii_uppercase

text = ''
FILE = open('pdf.txt', 'r').read()
for f in FILE:
    if f in ALLOWED:
        text += f

print(text)

'\''