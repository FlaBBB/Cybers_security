def get_key(cipher, know_message):
    len_know = len(know_message)
    len_cipher = len(cipher)
    brute_list = (
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z"
    )
    allowed_ord = (10,13)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    a_arr=[]
    b_arr=[]
    c_arr=[]
    d_arr=[]
    e_arr=[]
    f_arr=[]
    g_arr=[]
    h_arr=[]
    j_arr=[]
    for a in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 0:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        a_arr.append(a)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for b in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 1:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        b_arr.append(b)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for c in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 2:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        c_arr.append(c)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for d in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 3:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        d_arr.append(d)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for e in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 4:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        e_arr.append(e)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for f in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 5:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        f_arr.append(f)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for g in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 6:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        g_arr.append(g)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for h in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 7:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        h_arr.append(h)
    a = "-"
    b = "-"
    c = "-"
    d = "-"
    e = "-"
    f = "-"
    g = "-"
    h = "-"
    j = "-"
    for j in brute_list:
        cont = False
        key = a + b + c + d + e + f + g + h + j
        print("--try key: "+key, end="")
        for i in range(len_cipher):
            if i%len(key) != 8:
                continue
            dec = chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
            if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                cont = True
                break
        if cont:
            print(" ", end="\r")
            continue
        print(" Ok")
        j_arr.append(j)

    for a in a_arr:
        for b in b_arr:
            for c in c_arr:
                for d in d_arr:
                    for e in e_arr:
                        for f in f_arr:
                            for g in g_arr:
                                for h in h_arr:
                                    for j in j_arr:
                                        key = a + b + c + d + e + f + g + h + j
                                        print("-- TEST KEY: "+key+" --", end="")
                                        o = ''
                                        for i in range(len_cipher):
                                            o += chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
                                        if know_message not in o:
                                            print(" ", end="\r")
                                            continue
                                        print(" ")
                                        print(o+"\n\n")

    


cipher = "1020222c733a203a6c393d3769362d2520353121356907160c1b0a796f06213a306f263f782e722a3b222323293628376937263c262b362a3669272c6f28292c6f2b262663203d253d21262c3763382638306f3a26246317001e78383d3b3830614546102a202c74306f36232d3d722f3f2228756c0c1a111d153817001e077e761605701d16130a6b610f060f101b7c070c001003177f32"
get_key(bytes.fromhex(cipher).decode('utf-8'), "TUCTF{")
