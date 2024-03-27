from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from sage.all import QQ, ZZ, matrix, vector


def attack(y, k, s, m, a, c):
    """
    Recovers the states associated with the outputs from a truncated linear congruential generator.
    More information: Frieze, A. et al., "Reconstructing Truncated Integer Variables Satisfying Linear Congruences"
    :param y: the sequential output values obtained from the truncated LCG (the states truncated to s most significant bits)
    :param k: the bit length of the states
    :param s: the bit length of the outputs
    :param m: the modulus of the LCG
    :param a: the multiplier of the LCG
    :param c: the increment of the LCG
    :return: a list containing the states associated with the provided outputs
    """
    diff_bit_length = k - s

    # Preparing for the lattice reduction.
    delta = c % m
    y = vector(ZZ, y)
    for i in range(len(y)):
        # Shift output value to the MSBs and remove the increment.
        y[i] = (y[i] << diff_bit_length) - delta
        delta = (a * delta + c) % m

    # This lattice only works for increment = 0.
    B = matrix(ZZ, len(y), len(y))
    B[0, 0] = m
    for i in range(1, len(y)):
        B[i, 0] = a**i
        B[i, i] = -1

    B = B.LLL()

    # Finding the target value to solve the equation for the states.
    b = B * y
    for i in range(len(b)):
        b[i] = round(QQ(b[i]) / m) * m - b[i]

    # Recovering the states
    delta = c % m
    x = list(B.solve_right(b))
    for i, state in enumerate(x):
        # Adding the MSBs and the increment back again.
        x[i] = int(y[i] + state + delta)
        delta = (a * delta + c) % m

    return x


p = 3855732453396366484243
a = 735667146340350301943
b = 2743013456812077971216
out = [
    33,
    6,
    90,
    32,
    97,
    53,
    75,
    28,
    11,
    7,
    8,
    53,
    51,
    35,
    74,
    57,
    82,
    2,
    96,
    11,
    26,
    29,
    69,
    53,
    48,
    79,
    15,
    78,
    99,
    40,
    88,
    56,
    20,
    69,
    11,
    72,
    32,
    68,
    86,
    62,
    68,
    1,
    37,
    97,
    43,
    15,
    10,
    27,
    84,
    37,
    40,
    76,
    66,
    81,
    2,
    2,
    38,
    27,
    64,
    72,
    86,
    84,
    91,
    81,
    25,
    65,
    44,
    95,
    59,
    41,
    85,
    95,
]

cipher = "34daaa9f7773d7ea4d5f96ef3dab1bbf5584ecec9f0542bbee0c92130721d925f40b175e50587196874e14332460257b"

state_bit_length = 72
output_bit_length = 7

output = attack(out, state_bit_length, output_bit_length, p, a, b)
output = [o % 100 for o in output]
print(f"{output = }")
