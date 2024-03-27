print("Welcome to the greatest puzzlepalooza ever!")
print("Can you solve our puzzle without looking?")
s = input().encode()
if len(s) == 54:
    k = 0
    i = 0
    si128_arr = [int(x, 16) for x in "9baccb49fed06b08"]
    si128_arr = [int(x, 16) for x in "6995ae4bba65f79c"] + si128_arr
    si128_arr = [int(x, 16) for x in "6b4a18ed4ebcf308"] + si128_arr
    si128_arr = [int(x, 16) for x in "a8d9d3e542f4dee0"] + si128_arr
    si128_arr = [int(x, 16) for x in "16160e71494acf3c"] + si128_arr
    si128_arr = [0xA] + si128_arr
    si128 = 0
    for i in range(80, -1, -1):
        si128 |= si128_arr[i] << (4 * (80 - i))
    while True:
        if i >= 54:
            break
        s_i = s[i] - 64
        si128 ^= (s_i << (k & 7)) << ((k >> 3) * 8)  # [k >> 3]
        if (k & 7) > 2:
            si128 ^= (s_i >> (8 - (k & 7))) << (((k >> 3) + 1) * 8)  # [(k >> 3) + 1]
            print(hex(si128))
        k += 6
        i += 1
        if k == 324:
            if si128 & 0xF <= 8:
                j = 1
                is_continue = False
                while j != 81:
                    if (
                        ((si128 >> ((j >> 1) * 8)) >> (4 * (j & 1))) & 0xF
                    ) > 8:  # [j >> 1]
                        is_continue = True
                        break
                    j += 1
                if is_continue:
                    continue
