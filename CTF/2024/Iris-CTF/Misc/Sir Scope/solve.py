mapped = [
    0b10010110,
    0b01001110,
    0b10010110,
    0b11001110,
    0b11000110,
    0b00101110,
    0b01100110,
    0b01101110,
    0b00001100,
    0b11001110,
    0b10001100,
    0b00110110,
]


def seven_segement_displayer(l_map):
    string_list = ["" for _ in range(3)]
    for m in l_map:
        # m = ~m
        if m & 0b10000000:
            string_list[0] += " _ "
        else:
            string_list[0] += "   "
        if m & 0b01000000:
            string_list[1] += "|"
        else:
            string_list[1] += " "
        if m & 0b00100000:
            string_list[1] += "_"
        else:
            string_list[1] += " "
        if m & 0b00010000:
            string_list[1] += "|"
        else:
            string_list[1] += " "
        if m & 0b00001000:
            string_list[2] += "|"
        else:
            string_list[2] += " "
        if m & 0b00000100:
            string_list[2] += "_"
        else:
            string_list[2] += " "
        if m & 0b00000010:
            string_list[2] += "|"
        else:
            string_list[2] += " "
    for s in string_list:
        print(s)


seven_segement_displayer(mapped)
