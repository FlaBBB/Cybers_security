from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *

# nc 103.152.242.78 13338

HOST = "103.152.242.78"
PORT = 13338


BLOCK_SIZE = 16


class Local:
    def __init__(self):
        self.key = os.urandom(BLOCK_SIZE)

    def encrypt(self, plaintext: bytes):
        plaintext = pad(plaintext, BLOCK_SIZE)
        # print(plaintext)
        # forged = forging(plaintext[16:])
        # print([forged[i : i + BLOCK_SIZE] for i in range(0, len(forged), BLOCK_SIZE)])
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.decrypt(ciphertext)
        print(ciphertext)
        return unpad(ciphertext, BLOCK_SIZE)

    def sign_up(self, username: str):
        self.iv = os.urandom(BLOCK_SIZE)
        plaintext = '{"username": "' + username + '", "admin": false}'
        print(
            [
                plaintext[i : i + BLOCK_SIZE]
                for i in range(0, len(plaintext), BLOCK_SIZE)
            ]
        )
        return self.encrypt(plaintext.encode())


def sign_up(username):
    io.sendlineafter(b"M>", b"1")
    io.sendlineafter(b"username <<", username)
    io.recvuntil(b">>")
    return io.recvline().strip()


def sign_in(username, cookie):
    # print(f"{username = }")
    # print(f"{cookie = }")
    io.sendlineafter(b"M>", b"2")
    io.sendlineafter(b"username", username)
    io.sendlineafter(b"cookie", cookie)
    res = io.recvlines(2)[1]
    assert res == b"", res


def forging(cookie: bytes):
    block_cookies = [
        cookie[i : i + BLOCK_SIZE] for i in range(0, len(cookie), BLOCK_SIZE)
    ]
    target = b'A", "admin": tru'
    original = b'", "admin": fals'
    forged = xor(block_cookies[-3], target, original)
    block_cookies[-3] = forged

    return b"".join(block_cookies)


def attack(i):
    print(f"--- Attempt {i} ATTACK ---")
    cookie = bytes.fromhex(sign_up(USERNAME).decode())
    cookie = forging(cookie)
    sign_in(b"A" * (USERNAME_LEN - BLOCK_SIZE), cookie.hex().encode())
    io.sendlineafter(b"D>", b"2")
    flag = io.recvlines(2)[1].split(b": ")[1].strip().decode()
    print(f"flag: {flag}")
    io.close()


def test():
    print("--- TEST ---")
    local = Local()
    l_cookie = local.sign_up(USERNAME.decode())
    l_cookie = forging(l_cookie)
    print(f"forged-{l_cookie = }")
    res = local.decrypt(l_cookie)
    del local
    assert b'", "admin": true' in res
    print(f"result: {res}")
    print("--- END TEST ---")


USERNAME_LEN = BLOCK_SIZE + 2
print(f"{USERNAME_LEN = }")

USERNAME = b"A" * USERNAME_LEN

test()
print()
i = 1
while True:
    try:
        io = remote(HOST, PORT)
        attack(i)
        break
    except AssertionError:
        io.close()
        i += 1
        continue
