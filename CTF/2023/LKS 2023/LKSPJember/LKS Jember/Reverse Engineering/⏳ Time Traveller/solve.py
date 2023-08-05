# y (Years) < 2023
# 0 > m (Months) <= 12
# 0 > d (Days) <= 31

import string

the_list = [1371,
48,
117,
1363,
55,
107,
1293,
109,
88,
1373,
106,
88,
1364,
48,
35,
1288,
109,
88,
1358,
55,
108,
1357,
118]


# i used 2 as increament because the result of y * m * d is must odd (odd * even = even)
y = 1
while y < 2023:
    for m in range(1, 13, 2):
        for d in range(1, 32, 2):
            if y * m * d == 28077:
                temp = [y, m, d]
                for i in range(23):
                    res = chr(the_list[i] ^ temp[i % 3])
                    if res not in string.printable:
                        break
                    print(res, end="")
                print()
    y += 2