#!/bin/python

flag = 'tH1s_Fl4g_Ch3ckEr_sUr3_1S_W3iRd'
enc = []

for s in flag:
    enc.append((ord(s) << 4) ^ 0x1337)

print(enc)

enc = [5239, 6071, 4135, 5127, 5831, 5975, 5623, 4215, 5447, 5831, 5895, 5559, 4103, 5383, 5511, 5991, 5143, 5831, 5127, 5735, 5143, 4103, 5831, 4135, 5639, 5831, 5703, 4103, 5543, 5655, 5495]

for i in range(len(enc)):
    print(f'#define Section("f{i}") int _f{i} = {enc[i]};')