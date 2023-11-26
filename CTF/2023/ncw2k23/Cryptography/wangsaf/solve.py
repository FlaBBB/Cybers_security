from pwn import *
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

HOST = "103.145.226.209"
PORT = 1965

class attack:
    def __init__(self):
        self.io = remote(HOST, PORT)
        self.hello()
        self.param_handle()
    
    def client_send(self, data: bytes):
        self.io.sendlineafter(b"client (tamper):", data)
    
    def server_send(self, data: bytes):
        self.io.sendlineafter(b"server (tamper):", data)
        
    def recv(self):
        return self.io.recvline().strip().split(b": ")
    
    def encrypt(self, message, derived_key):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()

        ciphertext = iv + encryptor.update(padded_message) + encryptor.finalize()
        return base64.b64encode(ciphertext)

    def decrypt(self, message, derived_key):
        message = base64.b64decode(message)
        iv = message[:16]
        message = message[16:]
        cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(message) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        unpadded_message = unpadder.update(plaintext) + unpadder.finalize()

        return unpadded_message

    def deriveKey(self, shared_key):
        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
    
    def hello(self):
        self.client_send(b"hello!")
        self.server_send(b"hello!")
        
    def param_handle(self):
        recv_param = self.io.recvline().strip().split(b"||")[1]
        self.param = serialization.load_pem_parameters(bytes.fromhex(recv_param.decode()))
        self.attacker_private_key = self.param.generate_private_key()
        self.attacker_public_key = self.attacker_private_key.public_key()
        self.client_send(b"PARM||" + recv_param)
        self.server_send(b"PARM_ACC")
    
    def main(self):
        attacker_pubkey = self.attacker_public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
        
        recv_pubkey = self.io.recvline().strip()
        print(recv_pubkey)
        self.client_pubkey = serialization.load_pem_public_key(bytes.fromhex(recv_pubkey.split(b"||")[1].decode()), backend=default_backend())
        self.client_shared_key = self.attacker_private_key.exchange(self.client_pubkey)
        self.client_derive_key = self.deriveKey(self.client_shared_key)
        
        self.client_send(b"PUBK||" + attacker_pubkey.hex().encode())
        self.server_send(b"PUBK_ACC")
        
        recv_pubkey = self.io.recvline().strip()
        print(recv_pubkey)
        self.server_pubkey = serialization.load_pem_public_key(bytes.fromhex(recv_pubkey.split(b"||")[1].decode()), backend=default_backend())
        self.server_shared_key = self.attacker_private_key.exchange(self.server_pubkey)
        self.server_derive_key = self.deriveKey(self.server_shared_key)
        
        self.server_send(b"PUBK||" + attacker_pubkey.hex().encode())
        self.client_send(b"PUBK_ACC")
    
    def get_flag(self):
        code = self.encrypt("giv me the flag you damn donut", self.server_derive_key)
        self.client_send(code)
        return self.decrypt(self.recv()[1], self.server_derive_key).decode()


if __name__ == "__main__":
    attack = attack()
    attack.main()
    flag = attack.get_flag()
    print(f"{flag = }")