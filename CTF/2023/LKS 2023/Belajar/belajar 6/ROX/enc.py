import string, random, base64

def gen_key():
    k = ''.join([random.choice(string.ascii_letters) for x in range(0, 3)])
    print(k)
    return k

def _cipher(ky, pl):
    r = random.randint(0, 10)
    random.seed(r)
    cp = []
    for p in pl:
        cp.append(hex(ord(p) ^ ord(random.choice(ky))))
    return cp

if __name__ == "__main__":
    print(base64.b64encode(str(_cipher(gen_key(), input("Cipher : "))).encode("utf-8")).decode("utf-8"))
        
#cipher=WycweDI5JywgJzB4MjknLCAnMHgzMScsICcweDExJywgJzB4NTAnLCAnMHg1YicsICcweDU5JywgJzB4NzUnLCAnMHgzZScsICcweDJhJywgJzB4MjAnLCAnMHgyOCcsICcweDI2JywgJzB4MmUnLCAnMHgyZCcsICcweDFmJ10=