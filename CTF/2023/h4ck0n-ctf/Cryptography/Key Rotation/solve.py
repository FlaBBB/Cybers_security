from pwn import *
from sage.all import sqrt, matrix, vector

def to_matrix(s):
    res = []
    for i in s:
        temp = []
        for j in i[1:-1].strip().split(" "):
            if j != "":
                temp.append(int(j))
        assert len(temp) == len(s)
        res.append(temp)

    return matrix(res)

def rev_to_rotated_flag(flag):
    res = []
    for i in range(flag.nrows()):
        res.append(int(sqrt(flag[i][i])))
    return vector(res)

io = remote("64.227.131.98", 10001)

io.sendlineafter(b"(y/n)", b"y")

io.recvline()
rot_matrix = to_matrix(io.recvuntil(b"Printing Rotated Flag Matrix").decode().split("\n")[1:-1])
flag = []
while len(flag) != rot_matrix.nrows():
    temp = io.recvline().strip().decode()
    if temp != "":
        flag.append(temp)

flag = to_matrix(flag)
flag = rev_to_rotated_flag(flag)
flag = rot_matrix.solve_right(flag)
for i in flag:
    print(chr(i), end="")