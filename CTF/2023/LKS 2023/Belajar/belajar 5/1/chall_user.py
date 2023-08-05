import string
import hashlib
import random

flag  = "chaljariggkiarmvzxbppiqwrrsranrnga" # FLAG hanya terdiri dari ascii lowercase
arr   = list(string.ascii_lowercase)

def chain(center, num):
  return "".join(arr[(arr.index(x) + num) % 26 ] for x in center)

def change_center(left, right, center):
  lookup          = lambda x: arr.index(x)
  sum_left        = sum(map(lookup, left))
  sum_right       = sum(map(lookup, right))
  mul_left_right  = sum_left * sum_right
  modified_center = "".join(arr[(arr.index(x) + mul_left_right) % 26] for x in center)
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

    center = change_center(left, right, center)
  print(len(text))
  print(jump)
  print(init)
  print(left)
  print(right)
  return "".join(left_side + [center] + right_side)

# Fungsi untuk mengecek flag yang benar
def check(input_flag):
  if hashlib.md5(input_flag.encode()).hexdigest() == "c5b8e309ddaddd137182ccbafe61ad6d":
    print("Correct, The Flag is : JOINTS19{%s}" % (input_flag))
  else:
    print("Wrong Flag !")


# cipher = encrpyt(flag)
# print(cipher)
check("chaljariggkiarmvzxbppiqwrrsranrnga")
#cipher = "oubfbofgffkewddplnjafowyuuwfoxzovqxdkokxopootnfmmyuwsjoxfhddfoxgixezagnrnarsrrwqippbxzvmraikggirajlahcyelplypqppuognnzvxtkpygieegpyhjyfantaeanefeejdvccokmizenvxttvenwynupjpwawjabaafzryykgievajrtpprajsujqlmszdzmdeddicubbnjlhydmuwssudmvxmtoyelplypqppuognnzvxtkpygieegpyhjyfalrycylcdcchbtaamikgxcltvrrtcluwlsnoubfbofgffkewddplnjafowyuuwfoxzovqgmtxtgxyxxcwovvhdfbsxgoqmmoxgprgniekrvrevwvvaumttfbdzqvemokkmvenpelgagnrnarsrrwqippbxzvmraikggirajlahcekrvrevwvvaumttfbdzqvemokkmvenpelgntaeanefeejdvccokmizenvxttvenwynuplrycylcdcchbtaamikgxcltvrrtcluwlsnwcjnjwnonnsmellxtvrinwegccenwfhwdybgzkizqhffjhzqluywaoohpvqqrqzmqmfzotmxvmdusswumdyhljnbbuciddedmzdzsmqvozxofwuuywofajnlpddwekffgfobfbuolqjusjarpptrjaveigkyyrzfaabajwawpjmrkvtkbsqquskbwfjhlzzsagbbcbkxbxqkuzsdbsjayycasjenrpthhaiojjkjsfjfysmrkvtkbsqquskbwfjhlzzsagbbcbkxbxqkjohsqhypnnrphytcgeiwwpxdyyzyhuyunhotmxvmdusswumdyhljnbbuciddedmzdzsmzexigxofddhfxojswuymmfntoopoxkokdxfkdomduljjnldupycaessltzuuvudquqjdqvozxofwuuywofajnlpddwekffgfobfbuonslwulctrrvtlcxgkimaatbhccdclycyrldibmkbsjhhljbsnwaycqqjrxsstsbosohbdibmkbsjhhljbsnwaycqqjrxsstsbosohbxcvgevmdbbfdvmhquswkkdlrmmnmvimibvdibmkbsjhhljbsnwaycqqjrxsstsbosohbingrpgxommqogxsbfdhvvowcxxyxgtxtmglrycylcdcchbtaamikgxcltvrrtcluwlsnxdkokxopootnfmmyuwsjoxfhddfoxgixezjpwawjabaafzryykgievajrtpprajsujqllrycylcdcchbtaamikgxcltvrrtcluwlsnvbimivmnmmrldkkwsuqhmvdfbbdmvegvcxoubfbofgffkewddplnjafowyuuwfoxzovqlrycylcdcchbtaamikgxcltvrrtcluwlsnlrycylcdcchbtaamikgxcltvrrtcluwlsnwcjnjwnonnsmellxtvrinwegccenwfhwdypvcgcpghgglfxeeqmokbgpxzvvxgpyapwriovzvizazzeyqxxjfhduziqsooqzirtipkwcjnjwnonnsmellxtvrinwegccenwfhwdyiovzvizazzeyqxxjfhduziqsooqzirtipkflswsfwxwwbvnuugcearwfnpllnwfoqfmhagnrnarsrrwqippbxzvmraikggirajlahcmszdzmdeddicubbnjlhydmuwssudmvxmtobhosobstssxrjqqcyawnsbjlhhjsbkmbidingrpgxommqogxsbfdhvvowcxxyxgtxtmgnslwulctrrvtlcxgkimaatbhccdclycyrldibmkbsjhhljbsnwaycqqjrxsstsbosohbafyjhypgeeigypktxvznngouppqpylpleyqvozxofwuuywofajnlpddwekffgfobfbuoafyjhypgeeigypktxvznngouppqpylpleykpitrizqoosqizudhfjxxqyezzazivzvoiingrpgxommqogxsbfdhvvowcxxyxgtxtmgrwpaypgxvvzxpgbkomqeexflgghgpcgcvpafyjhypgeeigypktxvznngouppqpylpleyqvozxofwuuywofajnlpddwekffgfobfbuotyrcarizxxbzridmqosggzhniijireiexrbgzkizqhffjhzqluywaoohpvqqrqzmqmfzuzsdbsjayycasjenrpthhaiojjkjsfjfysuzsdbsjayycasjenrpthhaiojjkjsfjfystyrcarizxxbzridmqosggzhniijireiexrejcnlctkiimkctoxbzdrrksyttutcptpic"
