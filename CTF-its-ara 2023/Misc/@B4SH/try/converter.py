text = "ZIZ2023{4mby0wb_gs0f9sg_gs4g_!g5_4_s4hs?}"

converts = [{'Z':'A'},{'I':'R'}]
converted = ""
for t in text:
    breaks = False
    for convert in converts:
        for key in convert:
            if t == key:
                converted += convert[key]
                breaks = True
                break
        if breaks:
            break
    if not breaks:
        converted += t

print(converted)