#.data:0000000000004300 cicilan2        dd 'd', 'e', 'k', 'o', 'm', 'f', 'j', 'q', 'g', 'b', 'Q'
# .data:0000000000004300                                         ; DATA XREF: cek+2D↑o
# .data:0000000000004300                 dd 'L', 'N', '[', 's', '^', 'Y', 'J', '`', 'e', 'l', 'V'
# .data:0000000000004300                 dd 'Q', 'J', '_', 'b', 'Z', 'S', 2 dup('T'), 'V', 'C'
# .data:0000000000004300                 dd 'Q', 'G', 'H', 'L', 'T', '_', 'b', 'T', 'Z', 'S', '\'
# .data:0000000000004300                 dd 'W', 'H', 'O', 'A', 'U', 'T', ']', 'b', 'R', 'Y', 'I'
# .data:0000000000004300                 dd 'R', 'Q', 'R', 'J', 'M', 'D', '\'
# .data:0000000000004300 _data           ends

cicilan2 = ['d', 'e', 'k', 'o', 'm', 'f', 'j', 'q', 'g', 'b', 'Q',
            'L', 'N', '[', 's', '^', 'Y', 'J', '`', 'e', 'l', 'V',
            'Q', 'J', '_', 'b', 'Z', 'S', 'T', 'T', 'V', 'C',
            'Q', 'G', 'H', 'L', 'T', '_', 'b', 'T', 'Z', 'S', '\\',
            'W', 'H', 'O', 'A', 'U', 'T', ']', 'b', 'R', 'Y', 'I',
            'R', 'Q', 'R', 'J', 'M', 'D', '\\']

def nyicil(s):
    len_s = len(s)
    def cek(a, b, c, d):
        # You should implement the cek function according to its functionality
        # Since it's not provided, I'm assuming it returns some value here.
        # Replace this with the actual implementation.
        return 0

    if len_s <= 2:
        return 0xFFFFFFFFFFFFFFFF
    res = 0
    for i in range(len_s - 2):
        temp = 0
        for j in range(i, i + 3):
            temp += s[j]
        if cek(s[i] - temp // 3, s[i + 1] - temp // 3, s[i + 2] - temp // 3, temp // 3) == 128:
            res += 1
    return res

def main():
    print("SELAMAT DATANG di 'NYICIL'\n"
          "Disini anda diperintahkan untuk menyicil flag yang kemudian harus anda susun untuk mendapatkan flag secara utuh.")
    
    while True:
        s = input("masukan potongan flag, tulis \"stop\" jika dirasa sudah cukup: ")
        len_s = len(s)
        
        if s == "stop":
            break
        
        if len_s <= 10:
            hasil_nyicil = nyicil(list(map(ord, s)), len_s)
            if hasil_nyicil == -1:
                print("TIDAK DAPAT DITENTUKAN")
            elif hasil_nyicil == len_s - 2:
                print("BENAR!")
            elif hasil_nyicil:
                print("ADA YANG BENAR!")
            else:
                print("TIDAK BENAR!")
        else:
            print("Menyicil tidak perlu banyak")

if __name__ == "__main__":
    main()