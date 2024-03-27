from pwn import *

# nc 0.cloud.chals.io 26265
HOST = "0.cloud.chals.io"
PORT = 26265


def retrieve():
    return remote(HOST, PORT).recvall()


enc_flag = retrieve()
print(enc_flag)
print(len(enc_flag))
