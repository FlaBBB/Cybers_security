from sage.all import *


def long_to_str(x: int) -> str:
    return x.to_bytes((x.bit_length() + 7) // 8, "big").decode("latin-1")


N = 0x11B4C225F4DC385553FAEF71FD12D7A7D3731EEBB47D01DF2BD9C06CC95D67D933A3867DC3EF17547AE5A969DBC985489A3E835DDB0F8E1EB82B2CB84A5B168F74A808A0B7ACCBC1513CD416A5E8A4055A2823E192BDBE5DA3583B11B0A1697A5A47
e = 65537

n = 604928293513902242826844750697813298360296230589836965922445559460770464956330777297142978077171840381753362060166386141235478274641925844364093404007990669627544017237453555801510985434587758800309838580559380159655556994727763038972054055961008662617337727536706503888869143695786180320034250060574310562724453935738593360568145859518768293114591386063589064790586134071761566436891719201883451461515918132731425247986025975621160089191434740558642720428732247
u = 5124723399254519753965477778230820568274115995685406516489241951155141314318734047216941440562188021764716378577484405859111903738778224477333381592781148017098501746074849095701188434802818975767617255329420255949711066054049468803167
c = 310726350254360429088437156358460499035514323853708047519461603243147056286835156382941402126480154049593081421486020848538125531694986550091393457797356759194461290700917931171783019243503258123031885882322680819211732369309867241718158275015823673865567467449769107044499434442065689546731485951217928413599058868533165049407254866892923296832227322368063278457236148956502303822423581282369672779866499411399621396228547010983256343571496394052584949921815385

pbit = 512

# x = e^s
# x^3 + x + 1 - ux^2 = 0 (mod N)
P = Zmod(N)["x"]
(x,) = P._first_ngens(1)
f = x**3 + x + 1 - u * x**2

roots = f.roots()
print(f"{roots = }")

for i, _ in roots:
    s = Mod(i, N).log(e)
    if int(s).bit_length() < pbit:
        print(f"try {s = }")

        # p = n * s^-1 (mod 2^pbit)
        p = (n * inverse_mod(s, 2**pbit)) % 2**pbit
        print(f"{p = }")

        m = pow(c, inverse_mod(e, p - 1), p)

        flag = long_to_str(int(m))
        if "TCF2024{" not in flag:
            continue

        print(f"{flag = }")
        break