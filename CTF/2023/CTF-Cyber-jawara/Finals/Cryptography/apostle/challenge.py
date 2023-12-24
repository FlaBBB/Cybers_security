import copy
from hashlib import sha512
from os import urandom
from pprint import pprint

from aes import *
from Crypto.Util.strxor import strxor
from pwn import xor

FLAG = open("flag.txt", "rb").read()
master_key = urandom(16)
flag_key = sha512(master_key).digest()
enc_flag = strxor(FLAG, flag_key[: len(FLAG)])

plaintext = urandom(16)
plain_state = bytes2matrix(plaintext)
cipher_state = copy.deepcopy(plain_state)
key_matrices = expand_key(master_key, 1)
pprint(key_matrices)

add_round_key(cipher_state, key_matrices[0])
sub_bytes(cipher_state)
shift_rows(cipher_state)
cipher_state_shift = copy.deepcopy(cipher_state)
mix_columns(cipher_state)
add_round_key(cipher_state, key_matrices[1])

ciphertext = matrix2bytes(cipher_state)

print(f"Protected flag: {enc_flag.hex()}")
print(f"Plaintext: {plaintext.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")

print(f"Hint 1: {master_key[0]}")
print(f"Hint 2: {master_key[-1]}")
print(f"Hint 3: {master_key[-2]}")
