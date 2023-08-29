from Crypto.Util.number import *
import functools
from pwn import *
import time
from math import floor
import sys

sys.set_int_max_str_digits(100000)

def bytes2bin(msg: bytes):
    return bin(int.from_bytes(msg, "big"))[2:]

def bin2bytes(msg: bytes):
    return int(msg, 2).to_bytes((int(msg, 2).bit_length() + 7) >> 3, "big") or b"\x00"

class KeyGen:
    def __init__(self, x: int, m: int, c: int, n: int):
        self.m = m
        self.c = c
        self.n = n
        self.state = x % n
        self.bitstate = bin(self.state)[2:]

    def update_state(self, isflag=0):
        self.state = (self.state * self.m + self.c) % self.n
        self.bitstate = bin(self.state)[2:]
        if isflag:
            return
        time.sleep(1)
        
    def downdate_state(self):
        self.state = (self.state - self.c) * inverse(self.m, self.n) % self.n
        self.bitstate = bin(self.state)[2:]
        return self.state

    def get_bit(self, isflag=0):
        b = self.bitstate[-1]
        self.bitstate = self.bitstate[:-1]
        if not self.bitstate.isdigit():
            self.update_state(isflag)
        return int(b)

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(functools.reduce(GCD, zeroes))
    return crack_unknown_multiplier(states, modulus)

def enc_message(io, msg:bytes):
    io.sendlineafter(b'[>]', b'1')
    io.sendlineafter(b':', msg)
    start_time = time.time()
    res = bytes.fromhex(io.recvline().strip().decode().split(': ')[1])
    long_time = time.time() - start_time
    return res, floor(long_time)

def get_flag(io):
    io.sendlineafter(b'[>]', b'2')
    return bytes.fromhex(io.recvline().strip().decode().split(': ')[1])

def get_6_state(io):
    state = []
    half_first_state = None
    for _ in range(7):
        temp_state = ""
        while True:
            temp = enc_message(io, b'\x01')
            temp_state = str(int(temp[0].hex(), 16) ^ 1) + temp_state
            if temp[1] >= 1:
                if half_first_state == None:
                    half_first_state = temp_state
                else:
                    state.append(int(temp_state, 2))
                break
    return state, half_first_state

def decrypt_flag(io, ct):
    state, half_first_state = get_6_state(io)
    modulus, multiplier, increment = crack_unknown_modulus(state)
    print(f'[+] modulus = {modulus}')
    print(f'[+] multiplier = {multiplier}')
    print(f'[+] increment = {increment}')
    print(f'[+] half_first_state = {half_first_state}')
    key = KeyGen(state[0], multiplier, increment, modulus)
    keys = bin(key.downdate_state())[2:].replace(half_first_state, "")
    res = ""
    for i in bytes2bin(ct)[::-1]:
        res = str(int(i) ^ int(keys[0])) + res
        keys = keys[1:]
        if len(keys) == 0:
            keys = bin(key.downdate_state())[2:]
    return bin2bytes(res)

# nc 103.181.183.216 18000

io = remote('103.181.183.216', 18000)

flag = get_flag(io)
print(f'[+] flag = {flag.hex()}')
print(decrypt_flag(io, flag))