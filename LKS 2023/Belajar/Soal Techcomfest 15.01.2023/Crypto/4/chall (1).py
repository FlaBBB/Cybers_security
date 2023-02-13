
import random,string,hashlib

flag = "https://youtu.be/UIp6_0kct_U"
char = string.ascii_letters + string.digits
n = len(char)//2
d = 0.6
print(d)

def generate(n,d):
    max = 2 ** (n/d)
    what = [random.randrange(1,int(max)) for _ in range(n)]
    rahasia = [random.randrange(0,2) for _ in range(n)]
    res = sum(map(lambda i: i[0] * i[1], zip(what, rahasia)))
    return rahasia,what,res

def aku_mau_flag_dong(rahasia,tebak):
    w0w = ""
    i = 0
    while i < len(rahasia)*2: 
        w0w += char[i] if rahasia[i % len(rahasia)] else ""
        i += 1
    hashed = lambda x: hashlib.sha256(x.encode()).hexdigest()
    if hashed(w0w) != hashed(tebak):
        return False
    return True

rahasia,roger,sumatra = generate(n,d)
print('Nih kukasih roger sumatra aja dlu, klo mau flag minimal tau rahasianya')
print('roger = ', roger)
print('sumatra = ', sumatra)
tebak = input('rahasia = ')
if aku_mau_flag_dong(rahasia, tebak):
    print(f'hadehhh {flag}')
    exit(0)
exit(1)
