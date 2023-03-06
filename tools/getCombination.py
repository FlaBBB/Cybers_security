import math

def get_combinations_loop(lst, seed):
    n = len(lst)
    if seed <= n:
        return lst[seed-1]
    i = seed // n
    j = seed % n
    if j == 0:
        i -= 1
        j = n
    prev_combinations = get_combinations_loop(lst, i)
    last_element = lst[j-1]
    new_combinations = [c + last_element for c in prev_combinations]
    return new_combinations


def get_combinations_1(lst, seed):
    res = get_combinations_loop(lst, seed)
    if type(res) == list:
        return res[0]
    return res


def get_combinations_2(lst1, lst2, seed):
    res = get_combinations_loop(lst2, math.ceil(seed/len(lst1)))
    if type(res) == list:
        res = res[0]
    return lst1[(seed % len(lst1))-1]+res


lst1 = ['A', 'B', 'C']
lst2 = ['X', 'Y', 'Z']
for seed in range(1,100):
    combination = get_combinations_2(lst1, lst2, seed)
    print(combination)
