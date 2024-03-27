cipher = open("res-m", "rb").read()

cipher = [cipher[i : i + 8] for i in range(0, len(cipher), 8)]
print(cipher)
