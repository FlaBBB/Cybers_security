cipher = "!?}De!e3d_5n_nipaOw_3eTR3bt4{_THB"

flag = ""

for i in range(0, len(cipher), 3):
    flag += cipher[i + 2]
    flag += cipher[i]
    flag += cipher[i + 1]

flag = flag[::-1]
print(flag)
