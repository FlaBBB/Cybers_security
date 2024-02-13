import string

dictionary = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " "

encrypted_flag = "㭪䫴㭪ひ灮带⯠⯠孨囖抸櫲婾懎囖崼敶栴囖溚⾈牂"

for key in range(1, 501):
    flag = ""
    success = True
    for ch in encrypted_flag:
        ch = ord(ch)
        e = chr(ch // key)
        if e not in dictionary:
            success = False
            break
        flag += e
    if not success:
        continue
    print(key, flag)