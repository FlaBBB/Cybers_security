import string
import hashlib
import random

flag  = "chaljariggkiarmvzxbppiqwrrsranrnga" # FLAG hanya terdiri dari ascii lowercase
ASCII_LOWERCASE   = list(string.ascii_lowercase)

def chain(center, num):
  return "".join(ASCII_LOWERCASE[(ASCII_LOWERCASE.index(x) + num) % 26 ] for x in center)

def change_center(left, right, center):
  lookup          = lambda x: ASCII_LOWERCASE.index(x)
  sum_left        = sum(map(lookup, left))
  sum_right       = sum(map(lookup, right))
  mul_left_right  = sum_left * sum_right
  modified_center = "".join(ASCII_LOWERCASE[(ASCII_LOWERCASE.index(x) + mul_left_right) % 26] for x in center)
  return modified_center

def encrpyt(text):
  center      = text
  left_side   = []
  right_side  = []

  for jump in range(len(text)):
    init = random.randint(1,1337)
    if jump % 2 == 0:
      left        = chain(center, -init)
      right       = chain(center, init)[::-1]

      left_side  += [left]
      right_side  = [right] + right_side
    else:
      left        = chain(center, init)[::-1]
      right       = chain(center, -init)

      left_side   = [left] + left_side
      right_side += [right]
    print(left_side)
    print(right_side)

    center = change_center(left, right, center)

  return "".join(left_side + [center] + right_side)

cipher = encrpyt('aowkoawkoawkowakowkokaowkawokwaokwoawkoawkawowkoawkoawkawoawokawok')
print(cipher)
# cipher = "oubfbofgffkewddplnjafowyuuwfoxzovqxdkokxopootnfmmyuwsjoxfhddfoxgixezagnrnarsrrwqippbxzvmraikggirajlahcyelplypqppuognnzvxtkpygieegpyhjyfantaeanefeejdvccokmizenvxttvenwynupjpwawjabaafzryykgievajrtpprajsujqlmszdzmdeddicubbnjlhydmuwssudmvxmtoyelplypqppuognnzvxtkpygieegpyhjyfalrycylcdcchbtaamikgxcltvrrtcluwlsnoubfbofgffkewddplnjafowyuuwfoxzovqgmtxtgxyxxcwovvhdfbsxgoqmmoxgprgniekrvrevwvvaumttfbdzqvemokkmvenpelgagnrnarsrrwqippbxzvmraikggirajlahcekrvrevwvvaumttfbdzqvemokkmvenpelgntaeanefeejdvccokmizenvxttvenwynuplrycylcdcchbtaamikgxcltvrrtcluwlsnwcjnjwnonnsmellxtvrinwegccenwfhwdybgzkizqhffjhzqluywaoohpvqqrqzmqmfzotmxvmdusswumdyhljnbbuciddedmzdzsmqvozxofwuuywofajnlpddwekffgfobfbuolqjusjarpptrjaveigkyyrzfaabajwawpjmrkvtkbsqquskbwfjhlzzsagbbcbkxbxqkuzsdbsjayycasjenrpthhaiojjkjsfjfysmrkvtkbsqquskbwfjhlzzsagbbcbkxbxqkjohsqhypnnrphytcgeiwwpxdyyzyhuyunhotmxvmdusswumdyhljnbbuciddedmzdzsmzexigxofddhfxojswuymmfntoopoxkokdxfkdomduljjnldupycaessltzuuvudquqjdqvozxofwuuywofajnlpddwekffgfobfbuonslwulctrrvtlcxgkimaatbhccdclycyrldibmkbsjhhljbsnwaycqqjrxsstsbosohbdibmkbsjhhljbsnwaycqqjrxsstsbosohbxcvgevmdbbfdvmhquswkkdlrmmnmvimibvdibmkbsjhhljbsnwaycqqjrxsstsbosohbingrpgxommqogxsbfdhvvowcxxyxgtxtmglrycylcdcchbtaamikgxcltvrrtcluwlsnxdkokxopootnfmmyuwsjoxfhddfoxgixezjpwawjabaafzryykgievajrtpprajsujqllrycylcdcchbtaamikgxcltvrrtcluwlsnvbimivmnmmrldkkwsuqhmvdfbbdmvegvcxoubfbofgffkewddplnjafowyuuwfoxzovqlrycylcdcchbtaamikgxcltvrrtcluwlsnlrycylcdcchbtaamikgxcltvrrtcluwlsnwcjnjwnonnsmellxtvrinwegccenwfhwdypvcgcpghgglfxeeqmokbgpxzvvxgpyapwriovzvizazzeyqxxjfhduziqsooqzirtipkwcjnjwnonnsmellxtvrinwegccenwfhwdyiovzvizazzeyqxxjfhduziqsooqzirtipkflswsfwxwwbvnuugcearwfnpllnwfoqfmhagnrnarsrrwqippbxzvmraikggirajlahcmszdzmdeddicubbnjlhydmuwssudmvxmtobhosobstssxrjqqcyawnsbjlhhjsbkmbidingrpgxommqogxsbfdhvvowcxxyxgtxtmgnslwulctrrvtlcxgkimaatbhccdclycyrldibmkbsjhhljbsnwaycqqjrxsstsbosohbafyjhypgeeigypktxvznngouppqpylpleyqvozxofwuuywofajnlpddwekffgfobfbuoafyjhypgeeigypktxvznngouppqpylpleykpitrizqoosqizudhfjxxqyezzazivzvoiingrpgxommqogxsbfdhvvowcxxyxgtxtmgrwpaypgxvvzxpgbkomqeexflgghgpcgcvpafyjhypgeeigypktxvznngouppqpylpleyqvozxofwuuywofajnlpddwekffgfobfbuotyrcarizxxbzridmqosggzhniijireiexrbgzkizqhffjhzqluywaoohpvqqrqzmqmfzuzsdbsjayycasjenrpthhaiojjkjsfjfysuzsdbsjayycasjenrpthhaiojjkjsfjfystyrcarizxxbzridmqosggzhniijireiexrejcnlctkiimkctoxbzdrrksyttutcptpic"
# print(len(cipher))
