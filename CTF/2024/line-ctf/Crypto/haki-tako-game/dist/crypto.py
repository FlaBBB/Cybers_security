#!/usr/bin/env python3

# crypto challenge

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "./secret/"))
from server_secret import FLAG, MSG_FORMAT
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

AES_IV_HEX = "5f885849eadbc8c7bce244f8548a443f"
aes_iv = bytes.fromhex(AES_IV_HEX)


def cbc_decrypt(ciphertext, aes_key):
    cipher = AES.new(key=aes_key, mode=AES.MODE_CBC, iv=aes_iv)
    ret = {"ret": cipher.decrypt(ciphertext).hex()}
    return ret


def cfb128_decrypt(ciphertext, aes_key):
    cipher = AES.new(key=aes_key, mode=AES.MODE_CFB, iv=aes_iv, segment_size=128)
    ret = {"ret": cipher.decrypt(ciphertext).hex()}
    return ret


def truncated_cfb128_decrypt(ciphertext, aes_key):
    ret = cfb128_decrypt(ciphertext, aes_key)
    ret["ret"] = ret["ret"][: len(ret["ret"]) - (len(ret["ret"]) % 32)]
    for i in range(32, len(ret["ret"]) + 1, 32):
        ret["ret"] = ret["ret"][: i - 4] + "0000" + ret["ret"][i:]
    return ret


def generate_new_msg():
    aes_key = get_random_bytes(32)
    pin = get_random_bytes(256)
    msg = (
        b"Your authentication code is.."
        + pin
        + b". Do not tell anyone and you should keep it secret!"
    )
    return gcm_encrypt(msg, aes_key), pin, aes_key


def gcm_encrypt(plaintext, aes_key):
    nonce = get_random_bytes(12)
    cipher = AES.new(key=aes_key, mode=AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    ret = {"nonce": cipher.nonce.hex(), "ct": ciphertext.hex(), "tag": tag.hex()}
    return ret


def check_pin(pin, correct):
    if pin == correct.hex():
        return FLAG
    return ""
