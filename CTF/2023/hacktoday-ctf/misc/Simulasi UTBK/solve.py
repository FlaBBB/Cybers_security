from pwn import *
import json
from time import sleep

context.log_level = "warning"

# check if DICT_QUESTION.json exists
try:
    with open("DICT_QUESTION.json", "r") as f:
        DICT_QUESTION = json.load(f)
except:
    DICT_QUESTION = {}

while True:
    try:
        io = remote("103.181.183.216", 19003)
        life = 3
        point = 0
        while True:
            io.recvuntil(b"nyawa kamu")
            io.recvline()
            question = io.recvline().decode().strip()
            if question not in DICT_QUESTION:
                io.sendlineafter(b":", b"aaaaa")
                io.recvuntil(b"jawaban yang benar adalah ")
                answer = io.recvline().decode().strip()
                DICT_QUESTION[question] = answer
                point = 0
                life -= 1
            else:
                io.sendlineafter(b":", DICT_QUESTION[question].encode())
                temp = io.recvline().decode().strip()
                if "jawaban yang benar adalah " in temp:
                    point = 0
                    DICT_QUESTION[question] = temp.split("jawaban yang benar adalah ")[1]
                    life -= 1
                else:
                    point += 1
            if life == 0:
                io.close()
                break
            if point == 100:
                io.interactive()
                with open("DICT_QUESTION.json", "w") as f:
                    json.dump(DICT_QUESTION, f)
                exit()
    except KeyboardInterrupt:
        print("point: ", point)
        print("life: ", life)
        with open("DICT_QUESTION.json", "w") as f:
            json.dump(DICT_QUESTION, f)
        break
    except Exception as e:
        print("point: ", point)
        print("life: ", life)
        print("error: ", e)
        with open("DICT_QUESTION.json", "w") as f:
            json.dump(DICT_QUESTION, f)
        sleep(0.5)