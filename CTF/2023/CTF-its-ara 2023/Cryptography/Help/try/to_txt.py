def binary_to_text(binaryed):
    temp = ""
    text = ""
    for b in binaryed:
        if b == ' ':
            text += chr(int(temp, 2))
            temp = ""
        else :
            temp += b
    if len(temp) == 8:
        text += chr(int(temp, 2))
    return text

def brute():
    return

bina = "1011011 0111110 1100111 1001111 1000110 0001111 1000110 1110111 1110110 1011011 1001110 1001111 1110110 0111101 1001111 1110110 0001111 1001111 1011011 1011011 0001000 0000110 0001111 0001000 0000110 1011011 0001000 0110111 1001111 0110111 1001111"
print(binary_to_text(bina))