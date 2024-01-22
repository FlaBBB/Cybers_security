from Crypto.Util.number import long_to_bytes


def find_allowed(p_bit, q_bit):
    if p_bit == -1 and q_bit == -1:
        return [0, 1, 2, 3]
    elif p_bit == -1 and q_bit == 0:
        return [0, 2]
    elif q_bit == -1 and p_bit == 0:
        return [0, 1]
    elif p_bit == -1 and q_bit == 1:
        return [1, 3]
    elif q_bit == -1 and p_bit == 1:
        return [2, 3]
    elif p_bit == 0 and q_bit == 0:
        return [0]
    elif p_bit == 1 and q_bit == 0:
        return [2]
    elif p_bit == 0 and q_bit == 1:
        return [1]
    else:
        return [3]


def branch_and_prune(n, dna, p_bits, q_bits, s):
    solutions = [(1, 1)]
    loop_round = 1 + min(s, 1024 - s)
    for bit_pos in range(2, loop_round):
        next_solutions = []
        modulus = 2**bit_pos
        added = 2 ** (bit_pos - 1)
        target_n = n % modulus
        target_dna = dna % modulus
        accepted = find_allowed(p_bits[-bit_pos], q_bits[-bit_pos])
        for solution in solutions:
            pqs = [
                (solution[0], solution[1]),
                (solution[0], solution[1] + added),
                (solution[0] + added, solution[1]),
                (solution[0] + added, solution[1] + added),
            ]

            for i in accepted:
                p, q = pqs[i]
                if (p * q) % modulus == target_n and ((p & q) == target_dna):
                    next_solutions.append(pqs[i])

        solutions = next_solutions.copy()
        if solutions == []:
            break

    return solutions


n = 20316898932195904153277570911129808751568815578115203862825426326247688399447840960418077345063791379522152467572219078649052797300815169624324245983590614914067269781160218800744443132820786495383622657350005442865119235171347222481549171383138463856866590153226706585323109487068718209302113471433380661465050751463957327192775767168671487596946840993911799696944069759277414133632444513772210700794949276020219498655982617016744321984479076362225276288530893635176013522707993482886351558163399233902562390621254309853983712254751850630385079750216639722676398376824903099579116864460998259826947136455660974737633
dna = 112981924875557500958025001180130494828271302148393893025039250618449754880107262891213034570290994460680732065864408219699255537220809236513831561599199136870056419874815435027857448315805793914961273026882116413167515833581245087132919209478091324962372324771986076010340277554904109601589334046901209670673
enc = 3045339581292945711130813005351003100918522557110757541588006962379795819964889960982006172396478992403763951169397699477604011489683403206194674478676115307579754281253958928474112104087602753563505848223560038859380782692201785087834133116953880301903767021262497807797262966215767967235011554145888668721199447563741572273525508047234141844260401652933196055533764562153454963082569500478073362290691632890264262315099050876574517869170470080069161301450816555901477760392115210762498464643598219802952797283932722013302922244300834587051779128033516492433437534261890143822056118794447406885925957834712258842422

dna_bits = list(map(int, bin(dna)[2:].zfill(1024)))
is_found = False
p_bits = [1] + [-1 for _ in range(1022)] + [1]
q_bits = [1] + [-1 for _ in range(1022)] + [1]
for i in range(1, 1024):
    if dna_bits[i]:
        p_bits[i] = 1
        q_bits[i] = 1
for s in range(1024, 0, -1):
    shift = 1024 - s
    print(f"{shift = }")
    p_bits_, q_bits_ = p_bits.copy(), q_bits.copy()
    q_bits__ = p_bits_[s:] + p_bits_[:s]
    q_bits_ = [1 if (q_bits_[i] == 1 or q_bits__[i] == 1) else -1 for i in range(1024)]

    for i in range(1, 1024):
        if dna_bits[i] == 1:
            continue

        if p_bits_[i] == 1 and q_bits_[i] == -1:
            q_bits_[i] = 0
        elif q_bits_[i] == 1 and p_bits_[i] == -1:
            p_bits_[i] = 0
    res = branch_and_prune(n, dna, p_bits_, q_bits_, shift)
    if res == []:
        continue

    P.<x> = PolynomialRing(ZZ)
    for pair in res:
        if s <= 511: # q lsb
            f = (2 ** (1024 - s) * pair[1] + x) * (2 ** s * x + pair[1])
            d = f.roots()
            d = [k[0] for k in d if k[0] > 0]
            if d == []:
                continue
            p = 2 ** (1024 - s) * pair[1] + d[0]
        else:
            f = (2 ** (1024 - s) * x + pair[0]) * (2 ** s * pair[0] + x) - n
            d = f.roots()
            d = [k[0] for k in d if k[0] > 0]
            if d == []:
                continue
            p = 2 ** (1024 - s) * d[0] + pair[0]

        if n % p == 0:
            print(f'Found')
            q = n // p
            print(f'{p = }')
            print(f'{q = }')
            is_found = True
            break

    if is_found:
        break

d = pow(0x10001, -1, (p - 1) * (q - 1))
m = pow(enc, d, n)
print(long_to_bytes(int(m)))
