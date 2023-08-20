from pwn import *

# nc 0x7e7ctf.zerobyte.me 10027
HOST = "0x7e7ctf.zerobyte.me"
PORT = 10027

SALT_SIZE = 8

def enc(io, plaintext: bytes):
    io.sendlineafter(b"Masukkan pilihan: ", b"1")
    io.sendlineafter(b"Masukkan pesan: ", plaintext.hex().encode("latin-1"))
    return bytes.fromhex(io.recvline().decode().strip().split(": ")[-1])

def dec(io, ciphertext: bytes):
    io.sendlineafter(b"Masukkan pilihan: ", b"2")
    io.sendlineafter(b"Masukkan pesan terenkripsi: ", ciphertext.hex().encode("latin-1"))
    return io.recvline(timeout=5).strip().split(b": ")[-1]

def get_flag_size(io, enc_oracle, salt_size):
    last_len = len(enc_oracle(io, b""))
    flag_size = last_len - salt_size
    padding = b"A"
    while True:
        flag_size -= 1
        t_length = len(enc_oracle(io, padding))
        if t_length != last_len:
            break
        last_len = t_length
        padding += b"A"
    return flag_size

def attack(io, encrypt_oracle, decrypt_oracle, salt_size=8):
    flag_size = get_flag_size(io, encrypt_oracle, salt_size)

    padding_size = (16 * ((flag_size // 16) + 3)) - (flag_size + salt_size)
    padding = b"A" * padding_size
    cipher = encrypt_oracle(io, padding)

    offset_block = 1
    flag = b""
    while flag_size >= 16 or flag == b"":
        swapped_cipher = cipher[len(cipher) - (16 * (offset_block + 1)):len(cipher) - (16 * offset_block)] + cipher[16:]
        decrypted_text = decrypt_oracle(io, swapped_cipher)
        if flag == b"" and flag_size < 16:
            return decrypted_text[16 - flag_size:16]
        flag = decrypted_text[:16] + flag
        offset_block += 1
        flag_size -= 16

    if flag_size > 0:
        padding_size = (16 * ((flag_size // 16) + 3)) - (flag_size + salt_size) - (16 - flag_size)
        padding = b"A" * padding_size
        cipher = encrypt_oracle(io, padding)

        offset_block -= 1
        swapped_cipher = cipher[len(cipher) - (16 * (offset_block + 1)):len(cipher) - (16 * offset_block)] + cipher[16:]
        decrypted_text = decrypt_oracle(io, swapped_cipher)
        flag = decrypted_text[:flag_size] + flag

    return flag

io = remote(HOST, PORT)

print(attack(io, enc, dec))