from Crypto.Util.number import getPrime
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.number import bytes_to_long as b2l
from gmpy import next_prime
from secret import flag

FLAG = b2l(flag)

def prime():
    while True:
        prime =  getPrime(512)
        if(prime > FLAG):
            return prime

p = prime()
q = prime()
r = prime()

while True:
    s = prime()
    if(s>p and s>q and s>r):
        break

t = next_prime(s)

assert p > FLAG
assert q > FLAG
assert r > FLAG
assert s > FLAG

n = p*q*r*s*t

e = 0x10001
c = pow(FLAG,e,n)

print("c: ", c)
print("p*q*r :", p*q*r)
print("s*t :", s*t)

# ('c: ', 48040328963945990924620280027181859567719937668344126926458142380423140402374819358687273569544307175742204622093498945469754583990415151043215779435545223182628407118492962709105072438687997490923072400918252555673335579484667713859480270700396293189471353060838435749671529275805106294762039108113272362923503821551280307743557275641504472921295586138789905357356850005264836590347773376402713171124330977931453179566439465764966768958018036572327400394648382083423155479023011290236202665551696409477304131077159157381041203393813344449696881648681071375765006411243682683042845372880173162571694854512234885179623835923202849139558294792364724135312725706915598848116769946289581410042625417773048661635359465823610781769086404577379889085723323837023347656992603899L)
# ('p*q*r :', 730030886128526219689311100769234406418196980238863516575590522236272953024864242312259411513477181018732352144427347584200623942138397064688224971396043148742129540113222261838409958122091067588946234426847466527328571086530179583527040167641168587945601000314929671604003097524335572739036584490124771813393599604007933380169559919472645360424286707115046894610242995985236460083113149774847391601124466937151108551368099796680164040093837052494987905402846113L)
# ('s*t :', 159672486280615069155194159038074980974036988108999065911574227748097637460982188656226393140983755856628114482329643211169050408030104011052298880123059045016285641082771428955873527878281049469550087121014112061790150160811868518485274191226313948671751647131542221398655298649136877922755796240341752938893L)