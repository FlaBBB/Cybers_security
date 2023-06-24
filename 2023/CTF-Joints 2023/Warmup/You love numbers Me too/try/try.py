cipher = open("../542310").read()
while True:
    try:
        temp = ""
        for c in cipher.split(" "):
            temp += chr(int(c))
        cipher = temp
    except Exception as e:
        print(cipher)
        break