#!/usr/bin/python3
"""
Note: I used pycryptodome 3.16.0, if you had different version, sometimes it might arise an error
"""
from Crypto.Util.number import inverse, getPrime, isPrime, bytes_to_long, long_to_bytes
from base64 import urlsafe_b64decode as b64d, urlsafe_b64encode as b64e
from sympy.ntheory import sqrt_mod
import json, random, hashlib, uuid, time, os

FLAG = "final{anjay_final_semangat_bg}" if "FLAG" not in os.environ else os.environ['FLAG']

class Auth:
    def __init__(self, bit: int):
        self.q = 0
        while not self.q:
            self.p = getPrime(bit)
            self.q, self.g = next((((self.p - 1) // k, pow(2, k, self.p)) for k in range(2, 129) if not (self.p - 1) % k and isPrime((self.p - 1) // k)), (0, 0))

        self.x = random.randrange(2, self.q)
        self.y = pow(self.g, self.x, self.p)
    
    def __repr__(self):
        return f"{(b64e(long_to_bytes(self.p)).strip(b'=') + b'.' + b64e(long_to_bytes(self.g)).strip(b'=')).decode()}"

    def sbit(self, m: bytes) -> int:
        return sum([int(i) for i in bin(self.x ^ (bytes_to_long(m) % self.p))[2:]])

    def hash(self, m: bytes) -> int:
        return bytes_to_long(hashlib.sha256(m).digest())
    
    def verify(self, m: bytes, r: int, s: int) -> bool:
        def check_sig(s):
            t = pow(s, inverse(self.sbit(m), self.q - 1), self.q)
            u1 = pow(self.g, (self.hash(m) * inverse(t, self.q)) % self.q, self.p)
            u2 = pow(self.y, (r * inverse(t, self.q)) % self.q, self.p)
            return r == ((u1 * u2) % self.p) % self.q
        
        if (r < 2 or s < 2 or r > self.q or s > self.q): 
            return False
        if self.sbit(m) % 2:
            return check_sig(s)
        else:
            sq = sqrt_mod(s, self.q)
            return any(check_sig(s) for s in [sq, (-sq) % self.q])
    
    def signup(self, username: str, is_admin: bool=False) -> str:
        while True:
            cookie = b64e(json.dumps({'username': username, 'is_admin': is_admin, 'uuid': str(uuid.uuid1())}).encode()).strip(b'=')
            k = random.randrange(2, self.q - 2)
            r = pow(self.g, k, self.p) % self.q
            s = pow((self.hash(cookie) + self.x * r) * inverse(k, self.q), self.sbit(cookie) ,self.q)
            if self.verify(cookie, r, s):
                return (cookie + b'.' + b64e(long_to_bytes(r)).strip(b'=') + b'.' + b64e(long_to_bytes(s)).strip(b'=')).decode()

    def signin(self, username: str, cookie: str) -> dict:
        cookie, r, s = cookie.split('.')
        r = bytes_to_long(b64d(r + '=' * (4 - len(r) % 4)))
        s = bytes_to_long(b64d(s + '=' * (4 - len(s) % 4)))
        try:
            if self.verify(cookie.encode(), r, s):
                data = json.loads(b64d(cookie + '=' * (4 - len(cookie) % 4)))
            else:
                print("[!] broken cookie")
                return None
        except:
            print("[!] invalid cookie")
            return None
        if "uuid" not in data or len(data['uuid']) != 36 or data['uuid'].count("-") != 4:
            print("[!] invalid uuid")
            return None
        if "username" not in data or data['username'] != username:
            print("[!] invalid username")
            return None
        if "is_admin" not in data or data['is_admin'] not in [True, False]:
            print("[!] invalid role")
            return None
        return data
    
    
def main():
    print("[*] Wait for booting...", end="\r", flush=True)
    start = time.time()
    AUTH = Auth(512)

    print("[+] Boot took {:.2f} seconds".format(time.time() - start))
    print()
    print("[ Auth as a Service Again? ]")
    print("[ Support with public key: {} ]".format(AUTH))

    while True:
        try:
            print()
            print("(( menu ))")
            print("1. sign up")
            print("2. sign in")
            print("0. exit")

            match int(input("M> ")):
                case 1: 
                    print("cookie   >> {}".format(AUTH.signup(input("username << "))))
                case 2:
                    userdata = AUTH.signin(input("username << "), input("cookie   << "))
                    if userdata is not None:
                        if userdata['is_admin']:
                            print("\nWell deserved: {}".format(FLAG))
                            continue
                        else:
                            print("\nHi {}, there's nothing here, better you set is_admin = true. ~ciao~".format(userdata['username']))
                            continue
                    else: 
                        continue
                case 0: 
                    exit()
                case _:
                    print("[-] invalid choice")
                    
        except Exception as error:
            print(error)
            break

if __name__ == "__main__":
    main()