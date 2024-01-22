enc_flag = [110, 102, 118, 102, 115, 114, 118, 130, 103, 104, 92, 80, 98, 108, 63, 63, 65, 112, 113, 144]

flag = ""
for i, e in enumerate(enc_flag):
    flag += chr(e - i)

print(flag)