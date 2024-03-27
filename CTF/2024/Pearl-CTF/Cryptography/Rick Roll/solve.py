import string


def vignere_known_plaintext(cipher: str, known_plain: str) -> str:
    key = ""
    i = 0
    for c, kp in zip(cipher, known_plain):
        if c in string.ascii_lowercase:
            dif = ord("a")
        elif c in string.ascii_uppercase:
            dif = ord("A")
        else:
            continue

        if kp in string.ascii_lowercase:
            difa = ord("a")
        elif kp in string.ascii_uppercase:
            difa = ord("A")
        else:
            continue

        i += 1
        key += chr(((ord(c) - dif) - (ord(kp) - difa)) % 26 + ord("a"))
    return key


cipher = """Civvc Ihsce Gzgg Rtj Yp
Np'tx sd wtilpzjgw tf wqoj
Nsu byqp ywi rlwgl fch sf oq B
F uylc nqfrxxmvyv'l bwet Z'x vancoier qy Ddy wffnws'i kek ejbx uvod lpr tilei rwr N yysk hcgsp xecw ahz wsw Z'x
hxjamnx Rqmyp qabp ahz jrdvcumfch
Nvggk ldrnr rkoj nsu la Pxatv gfypt qtx yff fhbc
Rempt ztcra ifp twdynu lpw itweie ahz Civvc ihsce mrvg rtj grp
Ygojg koeyc lfn kofodrj
Civvc ihsce tvwn t qxi aeo jnwi col Hg'oj zrony gthw stypt ytg wo czpz
Ddyr ypcky'h fevy cvmxrg sfv rtj've kzq lmn xo jla by Xrszog pj qsty vphb llak'd dxjc kozyi hs
tzqo pdsdkft mr soyhzqyki zg xfqiqhzsqu
Wv vphb ile xlox fch wv'cg ztcra gwcr ni Enu th rtj esb xg atl M'm wpgenck
Dfy'v mjap mv jqn'wt xof mnbss xo jpg Gjkir xzpgf vmvv jqn ze
Rempt ztcra cpv rtj hony
Pxatv gfypt wjr aizwgi prd upuxwi col Ygojg koeyc ffzi yff ekd
Civvc ihsce srj ihtsfyv
Ygojg koeyc mjap a ctg tss luie ahz Civvc ihsce gzgg rtj yp
Epxxw vsnel nxy nsu uzyg
Stzei rqgsp vue lthzch aeo fxxtvt pzw Gjkir xzpgf bekv jqn hgc
Nvggk ldrnr dcr ldsdsjg
Gjkir xzpgf iilc l nbj prd yftm ddy Nvggk ldrnr rkoj, civvc ihsce gzgg (Znki yff wi)
(Tdl) Nvggk ldrnr rkoj, civvc ihsce gzgg (Znki yff wi) """

plain = """Never Gonna Give You Up
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm
feeling Gotta make you understand
Never gonna give you up Never gonna let you down
Never gonna run around and desert you Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you We've known each other for so long
Your heart's been aching but you're too shy to say it Inside we both know what's been going on"""

key = vignere_known_plaintext(cipher, plain)
print(key)
