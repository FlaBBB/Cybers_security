import os
from enum import Enum

from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad
from secret import FLAG


class Mode(Enum):
    ECB = 0x01
    CBC = 0x02


class Cipher:
    def __init__(self, key, iv=None):
        self.BLOCK_SIZE = 64
        self.KEY = [
            b2l(key[i : i + self.BLOCK_SIZE // 16])
            for i in range(0, len(key), self.BLOCK_SIZE // 16)
        ]
        self.DELTA = 0x9E3779B9
        self.IV = iv
        if self.IV:
            self.mode = Mode.CBC
        else:
            self.mode = Mode.ECB

    def _xor(self, a, b):
        return b"".join(bytes([_a ^ _b]) for _a, _b in zip(a, b))

    def encrypt(self, msg):
        msg = pad(msg, self.BLOCK_SIZE // 8)
        blocks = [
            msg[i : i + self.BLOCK_SIZE // 8]
            for i in range(0, len(msg), self.BLOCK_SIZE // 8)
        ]

        ct = b""
        if self.mode == Mode.ECB:
            for pt in blocks:
                ct += self.encrypt_block(pt)
        elif self.mode == Mode.CBC:
            X = self.IV
            for pt in blocks:
                enc_block = self.encrypt_block(self._xor(X, pt))
                ct += enc_block
                X = enc_block
        return ct

    def encrypt_block(self, msg):
        m0 = b2l(msg[:4])
        m1 = b2l(msg[4:])
        K = self.KEY
        msk = (1 << (self.BLOCK_SIZE // 2)) - 1

        s = 0
        for i in range(32):
            s += self.DELTA
            m0 += ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
            m0 &= msk
            m1 += ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3])
            m1 &= msk

        m = ((m0 << (self.BLOCK_SIZE // 2)) + m1) & (
            (1 << self.BLOCK_SIZE) - 1
        )  # m = m0 || m1

        return l2b(m)

    def decrypt(self, ct):
        blocks = [
            ct[i : i + self.BLOCK_SIZE // 8]
            for i in range(0, len(ct), self.BLOCK_SIZE // 8)
        ]

        msg = b""
        if self.mode == Mode.ECB:
            for ct in blocks:
                msg += self.decrypt_block(ct)
        elif self.mode == Mode.CBC:
            X = self.IV
            for ct in blocks:
                dec_block = self._xor(X, self.decrypt_block(ct))
                msg += dec_block
                X = ct
        return msg

    def decrypt_block(self, ct):
        m = b2l(ct)
        msk = (1 << (self.BLOCK_SIZE // 2)) - 1
        K = self.KEY

        s = (self.DELTA << 5) & msk
        m0 = (m >> (self.BLOCK_SIZE // 2)) & msk
        m1 = m & msk
        for i in range(32):
            m1 -= ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3])
            m1 &= msk
            m0 -= ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
            m0 &= msk
            s -= self.DELTA

        m = ((m0 << (self.BLOCK_SIZE // 2)) + m1) & ((1 << self.BLOCK_SIZE) - 1)

        return l2b(m)


if __name__ == "__main__":

    KEY = os.urandom(16)
    cipher = Cipher(KEY)
    ct = cipher.encrypt(FLAG)
    with open("output.txt", "w") as f:
        f.write(f"Key : {KEY.hex()}\nCiphertext : {ct.hex()}")