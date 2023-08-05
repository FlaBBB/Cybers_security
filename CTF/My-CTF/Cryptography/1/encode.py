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
    return [prev_combinations + [lst[j - 1]]]

def get_combinations(lst, seed):
    res = get_combinations_loop(lst, seed)
    if type(res) == list:
        return res[0]
    return [res]

def get_seed(lst):
    res = sum((max(lst) - min(lst) + 1) ** (len(lst) - i - 1) * (val - min(lst)) + (max(lst) - min(lst) + 1) ** i for i, val in enumerate(lst))
    assert get_combinations(range(min(lst), max(lst) + 1), res) == lst
    return res

def encode(plain):
    trash = []
    seed = []
    while len(plain) > 3:
        if len(plain) % 2 == 1:
            trash.append(ord(plain[-1]))
            plain = plain[:-1]
        templ = []
        tempt = ''
        for r in range(int(len(plain) / 2)):
            orded = ord(plain[int(len(plain) / 2 + r)])
            templ.append(orded)
            tempt += chr(ord(plain[r]) ^ orded)
        seed.append([get_seed(templ), min(templ), max(templ) + 1])
        plain = tempt
    with open('encoded.enc', 'w', encoding='utf-8') as ENC:
        ENC.write(plain + "\n" + str(trash).replace(']', '').replace('[', '') + "\n" + str(seed).replace(']', '').replace('[', ''))

encode('#REDACTED#')
