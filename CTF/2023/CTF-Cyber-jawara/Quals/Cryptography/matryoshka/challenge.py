import json
import os
from jose import jwe

KEY = os.urandom(16)

def encrypt(plaintext):
    return jwe.encrypt(plaintext, KEY, 'A128CBC-HS256', 'A128KW', 'DEF', 'application/json', '13337')

def decrypt(token):
    try:
        decrypted = jwe.decrypt(token, KEY)
        data = json.loads(decrypted)
        return data
    except Exception:
        return False

print(encrypt("abcdefghijklmnop"))