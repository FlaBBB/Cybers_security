import primefac
from math import gcd
import subprocess
import itertools
from sympy.ntheory.modular import crt

FLAG = 184521111987916661626689983056353649581579966522994882495441605638618755453

def factor_yafu(n):
    proc = subprocess.Popen("yafu", stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

    input_commands = ["factor({} - 1)".format(i) for i in n] + ["quit"]

    for command in input_commands:
        proc.stdin.write(command + "\n")
        proc.stdin.flush()

    output = proc.communicate()[0].split('***factors found***\n\n')[1:]
    res = []
    i = 0
    for o in output:
        if 'P' in o:
            res.append([])
            for line in o.split('ans =')[0].split('\n'):
                if 'P' in line:
                    res[i].append(int(line.split('P')[1].split(' = ')[-1]))
            i += 1

    return res

def factor(n):
    p = primefac.pollard_pm1(n)
    q = n // p
    res = {}
    p_factors, q_factors = factor_yafu([p, q])
    for i in p_factors + q_factors:
        if i not in res:
            res[i] = 0
        res[i] += 1
    
    return res, p_factors + q_factors, p, q, p_factors, q_factors

def chinese_remainder_theorem(congruences):
    N = 1
    for _, n in congruences:
        N *= n

    x = 0
    for a, n in congruences:
        Ni = N // n
        Mi = pow(Ni, -1, n)
        x = (x + a * Ni * Mi) % N

    return x

def pohlig_hellman(g, h, p, factors):
    congruences = []
    for prime, exponent in factors.items():
        q = prime ** exponent
        g_inv = pow(g, -1, q)
        h_i = (h * pow(g, -1, p)) % p
        discrete_log = 0
        for i in range(exponent):
            power = pow(g_inv, discrete_log, q)
            y_i = pow(h_i, q // prime**i, q)
            discrete_log += (y_i * power) % q
        congruences.append((discrete_log % q, q))
    
    x = chinese_remainder_theorem(congruences)
    return x

n = 15893901050264045030576295318430272352252281815013722598247809270793704029113291386554461448176708161197152486805731099740362102424820702477391865085386729579549728013515503349914268543068245180131117236009025659342860821398110622702511902409404556058796675635657989775085160845883717673427949837835434235551011049039593255958914584260486985515076377474512997597719112486042872649599426990887403348867209010345039952241251367918045902124711130057439189707428306101398482179024209099512036302115976765176396948621102223238546902865342025803338927409061735585597857957315802691357298583967779194995220682780038628912229
c = 4934347162688009464277147686290428901107185300990175242369558913357976689644445974379605421619983851888590849107437031010226914060746960360216539668681206285071439890419899517960816976926497942909414922431892044553420280953281972601275653702463521154180524665023322680435898557948097700621023726156126351702153865784390859811532108387835715301015901583962626955816902302006807499251813297248790995766380507715025994334051068564309907718570304525806757747026323543722492539064231073245947664818760382469348122697829075577680843135862206231697214708490549152098066062441709782221021641644777932943555638327450929660883

m = 3

f, p, q, p_factors, q_factors = factor(n)

phi = (p - 1) * (q - 1)

print(pohlig_hellman(m, c, n, f))

# print(res)