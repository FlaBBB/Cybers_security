import requests
import string

def attack(encrypt_oracle, unused_byte=0, known_prefix=b"", dictionary=None):
    """
    Recovers a secret which is appended to a plaintext and encrypted using ECB.
    :param encrypt_oracle: the encryption oracle
    :param unused_byte: a byte that's never used in the secret
    :return: the secret
    """
    paddings = [bytes([unused_byte] * i) for i in range(16)]
    secret = bytearray(known_prefix)
    while True:
        padding = paddings[15 - (len(secret) % 16)]
        p = bytearray(padding + secret + b"0" + padding)
        byte_index = len(padding) + len(secret)
        end1 = len(padding) + len(secret) + 1
        end2 = end1 + len(padding) + len(secret) + 1
        for i in range(256) if dictionary is None else dictionary:
            p[byte_index] = i
            c = encrypt_oracle(p)
            if c is None:
                continue
            if c[end1 - 16:end1] == c[end2 - 16:end2]:
                secret.append(i)
                print(bytes(secret))
                break
        else:
            secret.pop()
            break

    return bytes(secret)

def check(message: bytes) -> bool:
    for c in message:
        if c not in string.ascii_letters.encode("latin-1") + string.digits.encode("latin-1") + string.punctuation.encode("latin-1") + b" ":
            return False
    return True

def encrypt(message: bytes) -> bytes:
    message = bytes(message)
    if not check(message):
        return None
    r = requests.get("https://electronical.chall.pwnoh.io/encrypt", params={"message": message})
    return bytes.fromhex(r.text)

ctf_dictionary = [ord(c) for c in string.ascii_letters + string.digits + string.punctuation + " "]
res = attack(encrypt, ord("/"), b"bctf{", ctf_dictionary)
print(res)