import numpy as np
import random
from base64 import b64decode
from Crypto.Cipher import AES
import requests

# computational basis states
one_state = np.array([[1.0],[0.0]])
zero_state = np.array([[0.0],[1.0]])

# Hadamard and X-pauli gates
H = np.array([[1.0,1.0],[1.0,-1.0]])/np.sqrt(2), 
X = np.array([[0.0,1.0],[1.0,0.0]])

# print(H, X)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def get_quantum_key(state_list, basis_list, our_basis=None):
    key_bits = ''   
    
    if(len(state_list) != 1024 or len(basis_list) != 1024):
        return -1
    
    for basis in basis_list:
        if(str.upper(basis) not in ['H', 'X']):
            return -1

    if(our_basis == None):
        our_basis = []
                        
        for i in range(0, 1024):
            our_basis.append(random.choice(["H", "X"]))
            
    for i in range(0, 1024):
        if(our_basis[i] == basis_list[i]):
            if(basis_list[i] == "H"):
                state = np.dot(H, state_list[i])
            else:
                state = [np.dot(X, state_list[i])]

            # print(state_list[i], state)
            if(state[0][0] > .99):
                key_bits += '1'
            else:
                key_bits += '0'
    
    if(len(key_bits) < 128):
        return -1
    
    key = bitstring_to_bytes(key_bits[0:128])
    
    return key

state = []
state_np = []
for _ in range(1024):
    if random.choice([True, False]):
        state.append([0,1])
        state_np.append(zero_state)
    else:
        state.append([1,0])
        state_np.append(one_state)

basis_list = ["X"] * 1024

def decrypt(ciphertext, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

URL = "https://nessus-quantumcrypto.chals.io/quantum_key"

r = requests.post(URL, json={"state_list":state, "basis_list":basis_list})

r_json = r.json()
key = get_quantum_key(state, basis_list, r_json["basis"])

print(decrypt(b64decode(r_json["ciphertext"]), b64decode(r_json["iv"]), key))