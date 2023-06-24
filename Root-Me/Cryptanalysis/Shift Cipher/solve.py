import string
cp = open('ch7.bin', 'rb').read()

def bruteshift(cp):
    res = {}
    for i in range(256):
        plain = ''
        score = len(cp)
        for c in cp:
            if type(c) != int:
                c = ord(c)
            temp = chr((c - i) % 255) 
            if temp not in string.printable:
                score -= 1
            plain += temp
        if res.get(score) == None:
            res[score] = []
        res[score].append((plain, i))
    return dict(sorted(res.items())[::-1])
        
    
def get_key(cp, i):
    key = ''
    for c in cp:
        if type(c) != int:
            c = ord(c)
        key += chr((c - i) % 255)
    return key


print(get_key(cp, 10))
# res = bruteshift(cp)
# for r in res:
#     print(res[r])
#     print()