import sys
import string


def get_combination(a, b):
    temp = []
    for x in a:
        for y in b:
            temp.append(x+y)
    return temp


def brute(cipher, len_key, know_message="", allowed_ord=[]):
    len_cipher = len(cipher)
    len_know = len(know_message)

    if len_cipher < len_know:
        print("\n-- Brute Failed, Please check your input --")
        return False

    orginal_know_message = know_message
    if len_know > len_key:
        len_know = len_key
        know_message = know_message[:len_key]

    brute_list = [s for s in string.ascii_letters + string.digits + string.punctuation]

    array = dict()
    for z in range(len_key):
        array[brute_list[z]] = "-"
        array[brute_list[z]+"_array"] = []

    for z in know_message:
        array[z+"_loc"] = dict()

    for z in range(len_key):
        if z != 0:
            array[brute_list[z-1]] = "-"
        for a in brute_list:
            array[brute_list[z]] = a
            cont = False
            key = ""
            for b in range(len_key):
                key += array[brute_list[b]]
            dump = dict()
            for i in range(len_cipher):
                if i % len_key != z:
                    continue
                dec = chr(ord(cipher[i]) ^ ord(key[i % len_key]))
                if not (dec.isprintable() or (ord(dec) in allowed_ord)):
                    cont = True
                    break
                else:
                    if dec in know_message:
                        if dump.get(dec) == None:
                            dump[dec] = dict()
                        if dump[dec].get(str(z)) == None:
                            dump[dec][str(z)] = dict()
                        if dump[dec][str(z)].get(i) == None:
                            dump[dec][str(z)][i] = dict()
                        dump[dec][str(z)][i] = a
            if cont:
                continue
            print("- try key: "+key+" Ok")
            array[brute_list[z]+"_array"].append(a)
            for dec in dump:
                for order in dump[dec]:
                    for k in dump[dec][order]:
                        if array[dec+"_loc"].get(order) == None:
                            array[dec+"_loc"][order] = dict()
                        if array[dec+"_loc"][order].get(k) == None:
                            array[dec+"_loc"][order][k] = dict()
                        array[dec+"_loc"][order][k] = dump[dec][order][k]

    print("\n")
    for z in range(len_key):
        print("key offset "+str(z)+" = ", end="")
        print(array[brute_list[z]+"_array"])

    print("\n")
    print(
        "-- Location every letter of knowed words {<key_offset> : {<offset on word> : <key on key_offset>}}")
    for z in know_message:
        print("~ location '"+z+"' = ", end="")
        print(array[z+"_loc"])

    key_i = 0
    key_valid_list = []
    for z in range(len_key):
        if array[know_message[0]+"_loc"].get(str(z)) == None:
            continue
        for a in array[know_message[0]+"_loc"][str(z)]:
            last_offset = None
            cont = False
            fixed_key = ""
            for b in range(len_know):
                if last_offset == None:
                    last_offset = a
                    fixed_key += array[know_message[b]+"_loc"][str(z)][a]
                    continue
                if array[know_message[b]+"_loc"].get(str((z+b) % len_key)) == None:
                    cont = True
                    break
                if (last_offset+1) in array[know_message[b]+"_loc"][str((z+b) % len_key)]:
                    last_offset += 1
                    fixed_key += array[know_message[b] + "_loc"][str((z+b) % len_key)][last_offset]
                else:
                    cont = True
                    break
            if cont:
                continue
            key_valid_list.append(dict())
            key_valid_list[key_i][z] = fixed_key
            key_i += 1

    print("\n")
    print("-- list valid key ({<offset_key_place> : <key>})")
    print(key_valid_list)

    if key_valid_list == []:
        print("\n-- Brute Failed, Please check your input --")
        return False

    if len(key_valid_list) > 1:
        print("\n")
        print("result valid key is more than 1, you must choose 1 from the list")
        print("valid key list:")
        i = 1
        for a in key_valid_list:
            for b in a:
                print(str(i)+". "+a[b])
            i += 1
        try:
            inp = int(input("choose the valid key you want try: "))
            assert key_valid_list[inp-1] != None
            temp_valid_key = key_valid_list[inp-1]
            key_valid_list = []
            key_valid_list.append(temp_valid_key)
        except:
            sys.exit("your input not available in the list!!!")
    key_arr = []
    for z in key_valid_list:
        for b in z:
            key_valid = z[b]
            key_offset = b
        key = []
        for a in range(len_key):
            if ((key_offset+len_know) > len_key) and a < (len(key_valid)-(len_key - key_offset)):
                if key == []:
                    key = [key_valid[(len_key-key_offset)+a]]
                else:
                    key = get_combination(key, key_valid[(len_key-key_offset)+a])
            elif (a >= key_offset) and (a < key_offset+len_know):
                if key == []:
                    key = [key_valid[a-key_offset]]
                else:
                    key = get_combination(key, key_valid[a-key_offset])
            else:
                if key == []:
                    key = array[brute_list[a]+"_array"]
                else:
                    key = get_combination(key, array[brute_list[a]+"_array"])
        for c in key:
            key_arr.append(c)

    print("\n")
    for key in range(len(key_arr)):
        print("- TEST KEY ("+str(key)+"): "+key_arr[key]+" -", end="")
        o = ''
        for i in range(len_cipher):
            o += chr(ord(cipher[i]) ^ ord(key_arr[key][i % len_key]))
        if orginal_know_message not in o:
            print(" ", end="\r")
            continue
        print(" ")
        print(o+"\n\n")

    return True


# -- MAIN --
cipher = "1020222c733a203a6c393d3769362d2520353121356907160c1b0a796f06213a306f263f782e722a3b222323293628376937263c262b362a3669272c6f28292c6f2b262663203d253d21262c3763382638306f3a26246317001e78383d3b3830614546102a202c74306f36232d3d722f3f2228756c0c1a111d153817001e077e761605701d16130a6b610f060f101b7c070c001003177f32"
brute(bytes.fromhex(cipher).decode(), 9, "Hope you", [10])
