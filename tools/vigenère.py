import string
from nostril import nonsense
from tqdm import tqdm

DICTIONARY = [i for i in string.ascii_lowercase]


def get_combinations_loop(lst: list, seed: int) -> str | list:
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


def get_combinations(lst: list, seed: list) -> str:
    res = get_combinations_loop(lst, seed)
    if type(res) == list:
        return res[0]
    return res


def vignere_encrypt(plain: str, key: str) -> str:
    cipher = ""
    i = 0
    for p in plain:
        k = key[i % len(key)]
        if p in string.ascii_lowercase:
            dif = ord('a')
        elif p in string.ascii_uppercase:
            dif = ord('A')
        else:
            cipher += p
            continue

        if k in string.ascii_lowercase:
            difa += ord('a')
        elif k in string.ascii_uppercase:
            difa += ord('A')
        else:
            raise "key must be alphabet characters"

        i += 1
        cipher += chr((ord(p) + ord(k) - difa) % 26 + dif)
    return cipher


def vignere_decrypt(cipher: str, key: str) -> str:
    plain = ""
    i = 0
    for c in cipher:
        k = key[i % len(key)]
        if c in string.ascii_lowercase:
            dif = ord('a')
        elif c in string.ascii_uppercase:
            dif = ord('A')
        else:
            plain += c
            continue

        if k in string.ascii_lowercase:
            difa += ord('a')
        elif k in string.ascii_uppercase:
            difa += ord('A')
        else:
            raise "key must be alphabet characters"

        i += 1
        plain += chr((ord(c) - (ord(k) - difa)) % 26 + dif)
    return plain


def vignere_bruteforce(cipher: str, attempts_seed: int | bytes = 1000000) -> tuple | None:
    if type(attempts_seed) == bytes:
        attempts_seed = len(DICTIONARY) ** int(attempts_seed, 2)
    for seed in tqdm(range(1, attempts_seed + 1)):
        key = get_combinations(DICTIONARY, seed)
        
        plain = ""
        i = 0
        for c in cipher:
            k = key[i % len(key)]
            if c in string.ascii_lowercase:
                dif = ord('a')
            elif c in string.ascii_uppercase:
                dif = ord('A')
            else:
                try:
                    if nonsense(plain):
                        break
                except Exception as e:
                    if e != "Text is too short to test":
                        raise e
                plain += c
                continue

            if k in string.ascii_lowercase:
                difa += ord('a')
            elif k in string.ascii_uppercase:
                difa += ord('A')
            else:
                raise "key must be alphabet characters"

            i += 1
            plain += chr((ord(c) - (ord(k) - difa)) % 26 + dif)
        
        try:
            if nonsense(plain):
                continue
        except Exception as e:
            if e != "Text is too short to test":
                raise e
            
        return (key, plain)
    return None
