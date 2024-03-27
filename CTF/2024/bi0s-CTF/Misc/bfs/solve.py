from pwn import *

HOST = "13.201.224.182"
PORT = 31412

r = remote(HOST, PORT)


def level_1_init():
    r.sendlineafter(b"Your choice : ", b"N")
    r.sendlineafter(b"Your choice : ", b"N")


def level_1():
    up = "+[>[<-]<[->+<]>]>[<-[>[-<+>]]<]"
    down = "+[<[>-]>[-<+>]<]<[>-[<[->+<]]>]"
    r.recvuntil(b"THERE IS A BYTE OF THE FLAG DROPPED AT INDEX OF TAPE >")
    pt = eval(r.recvline().strip().decode())[0]

    r.recvuntil(b"DATA POINTER IS AT : ")
    cur = int(r.recvline().strip().decode())
    payload = up if cur < pt else down
    r.sendlineafter(b"INPUT YOUR CODE :", payload.encode())
    r.recvuntil(b"DATA POINTER AT -")
    res = int(r.recvline().strip().decode())
    return chr(abs(res - pt))


def level_1_skip():
    level_1_init()
    for _ in range(19):
        up = "+[>[<-]<[->+<]>]"
        down = "+[<[>-]>[-<+>]"
        r.recvuntil(b"THERE IS A BYTE OF THE FLAG DROPPED AT INDEX OF TAPE >")
        pt = eval(r.recvline().strip().decode())[0]

        r.recvuntil(b"DATA POINTER IS AT : ")
        cur = int(r.recvline().strip().decode())
        payload = up if cur < pt else down
        r.sendlineafter(b"INPUT YOUR CODE :", payload.encode())


def level_2_init():
    r.sendlineafter(b"Your choice : ", b"N")


def level_2():
    # `{}` will be replace with `+` and the number of it will depend on how much jump we need to do (rip english)
    up = ">{}[>[<-[[->>+<<]>>>]]<[->+<]>]>."
    down = "<{}[<[>-[[-<<+>>]<<<]]>[-<+>]<]<."
    r.recvuntil(
        "▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭▭".encode()
    )
    tseq = (
        r.recvlines(2)[1].strip().decode().replace("[", "").replace("]", "").split(" ")
    )
    tseq = list(map(int, tseq))

    r.recvuntil(b"DATA POINTER IS AT : ")
    tseq.insert(0, int(r.recvline().strip().decode()))

    dseq = {s: i for i, s in enumerate(sorted(tseq))}
    seq = [(s, dseq[s]) for s in tseq]

    payload = "+"
    cur = None
    cur_ord = None
    for s, s_ord in seq:
        if cur is not None:
            if cur < s:
                payload += up.format("+" * abs(s_ord - cur_ord))
            else:
                payload += down.format("+" * abs(s_ord - cur_ord))
        cur = s
        cur_ord = s_ord

    r.sendlineafter(b"INPUT YOUR CODE :", payload.encode())

    r.recvuntil(b"-> ")
    return r.recvuntil(b" <-").strip().strip(b" <-").decode()


def level_2_skip():
    level_2_init()
    level_2()


def move_pointer(start, end):
    if start < end:
        return ">" * (end - start)
    else:
        return "<" * (start - end)


def level_3(knowed=""):
    global r
    context.log_level = "warning"
    fmove_up = "+[>[<-]<[->+<]>]>"
    fmove_down = "+[<[>-]>[-<+>]<]<"
    move_cflag_up = "[>[<-[->+<]]<[->+<]>]>"
    move_cflag_down = "[<[>-[-<+>]]>[-<+>]<]<"
    mod_2 = "<<+>>[-[-<]>]<<<+>[-]<"
    fdevide_2 = "<<+>>[-[-<<+>]>]<<[>]<-"
    check = "-[<]"
    decrement_down = "[-<[>-[-<+>]]>[-<+>]<]"

    res = knowed
    for i in range(len(knowed), 18):
        cflag = 0
        for j in range(7):  # limit by 7 bits
            t = 0
            while True:
                try:
                    r.close()
                    r = remote(HOST, PORT)
                    level_1_skip()
                    level_2_skip()

                    for _ in range(i):
                        r.recvuntil(
                            b"THERE IS A BYTE OF THE FLAG DROPPED AT INDEX OF TAPE > "
                        )
                        pt = eval(r.recvline().strip().decode())[0]
                        r.recvuntil(b"THE DATA POINTER WILL INITIALLY BE AT ")
                        cur = eval(r.recvline().strip().decode())[0]
                        payload = fmove_up if cur < pt else fmove_down
                        r.sendlineafter(b"INPUT YOUR CODE :", payload.encode())

                    r.recvuntil(b"THE DATA POINTER WILL INITIALLY BE AT ")
                    cur = eval(r.recvline().strip().decode())[0]

                    payload = "<" * cur + "+>" + fmove_up
                    for _ in range(j):
                        payload += fdevide_2
                    payload += mod_2
                    payload += move_cflag_down
                    payload += check
                    r.sendlineafter(b"INPUT YOUR CODE :", payload.encode())

                    if b"ERROR" in r.recvline().strip():
                        cflag |= 1 << j
                    break
                except:
                    if t > 3:
                        raise
                    t += 1
        res += chr(cflag)
        print(f"[*] {i + 1}/19: {res[-1]}")
    return res


level_1_init()
flag = ""
for _ in range(19):
    flag += level_1()

level_2_init()
flag += level_2()
flag += level_3("m_Tur1ng_c0Mplet3}")

print(flag)  # bi0sctf{M4yb3_I_M1sint3rpret3d_th3_t3rm_Tur1ng_c0Mplet3}
