import string
import random
import base64

ASCII_LETTER = string.ascii_letters
ALLOWED = string.ascii_letters+string.digits+string.punctuation

def get_combinations_loop(lst, seed):
    n = len(lst)
    if seed <= n:
        return lst[seed-1]
    i = seed // n
    j = seed % n
    if j == 0:
        i -= 1
        j = n
    prev_combinations = [get_combinations_loop(lst, i)]
    while type(prev_combinations[0]) == list:
        prev_combinations = prev_combinations[0]
    last_element = lst[j-1]
    new_combinations = [c + last_element for c in prev_combinations]
    return new_combinations


def get_combinations(lst, seed):
    res = get_combinations_loop(lst, seed)
    if type(res) == list:
        return res[0]
    return res


def brute(cipher, know_char = False):
    res = []

    for c in cipher:
        res.append(int(c,16))

    if know_char:
        if len(know_char) > len(res):
            return 0
        elif len(know_char) == len(res):
            print(know_char)
            return 0

    seed = 2757
    i = 1
    try1 = 1
    while True:
        key = get_combinations(list(ASCII_LETTER), seed)
        seed += 1
        if len(key) < 3:
            continue
        elif len(key) > 3:
            break

        for r in range(11):
            print(f"Try {try1}", end='\r')
            try1 += 1
            random.seed(r)
            is_continue = False
            text = ''
            for x, c in zip(range(len(res)),res):
                temp = chr(c ^  ord(random.choice(key)))
                if temp not in ALLOWED:
                    is_continue = True
                    break
                if know_char:
                    if not x >= len(know_char):
                        if temp != know_char[x]:
                            is_continue = True
                            break
                text += temp
            if know_char:
                if know_char not in text:
                    is_continue = True

            if is_continue:
                continue
            print(i,'=',text,'-- key =',key)
            i += 1

cipher = 'WycweDI5JywgJzB4MjknLCAnMHgzMScsICcweDExJywgJzB4NTAnLCAnMHg1YicsICcweDU5JywgJzB4NzUnLCAnMHgzZScsICcweDJhJywgJzB4MjAnLCAnMHgyOCcsICcweDI2JywgJzB4MmUnLCAnMHgyZCcsICcweDFmJ10='
if __name__ == '__main__':
    brute(base64.b64decode(cipher.encode()).decode().replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(','), 'KKST')
