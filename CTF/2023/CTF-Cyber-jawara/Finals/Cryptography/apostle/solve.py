import copy
from functools import reduce
from hashlib import sha512
from os import urandom

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


def sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


def inv_sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]


def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
def xtime(a): return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)
    
def inv_mix_single_column(a):
    for _ in range(3):
        mix_single_column(a)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])


def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)


def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i + 4]) for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))


def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return list(i ^ j for i, j in zip(a, b))


def inc_bytes(a):
    """ Returns a new byte array with the value increment by 1 """
    out = list(a)
    for i in reversed(range(len(out))):
        if out[i] == 0xFF:
            out[i] = 0
        else:
            out[i] += 1
            break
    return bytes(out)


def pad(plaintext):
    """
    Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
    Note that if the plaintext size is a multiple of 16,
    a whole block will be added.
    """
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding


def unpad(plaintext):
    """
    Removes a PKCS#7 padding, returning the unpadded text and ensuring the
    padding was correct.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message


def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i + 16] for i in range(0, len(message), block_size)]


def expand_key(master_key, n_rounds):
    key_columns = bytes2matrix(master_key)
    # print(key_columns)
    iteration_size = len(master_key) // 4

    # Each iteration has exactly as many columns as the key material.
    columns_per_iteration = len(key_columns)
    i = 1
    while len(key_columns) < (n_rounds + 1) * 4:
        # Copy previous word.
        word = list(key_columns[-1])

        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift.
            word.append(word.pop(0))
            # Map to S-BOX.
            # print("1: ", word)
            word = [s_box[b] for b in word]
            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            # print("2: ", word)
            word[0] ^= r_con[i]
            i += 1
        elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
            # Run word through S-box in the fourth iteration when using a
            # 256-bit key.
            word = [s_box[b] for b in word]

        # print("3: ", word)
        # XOR with equivalent word from previous iteration.
        word = xor_bytes(word, key_columns[-iteration_size])
        # print("4: ", word)
        key_columns.append(word)

    # Group key words in 4x4 byte matrices.
    return [key_columns[4 * i: 4 * (i + 1)] for i in range(len(key_columns) // 4)]


from Crypto.Util.strxor import strxor
from tqdm import tqdm


def xor(*args):
    return [reduce(lambda x, y: x ^ y, v) for v in zip(*args)]


FLAG = b"FLAG{"
FLAG = FLAG + b"#" * (16 - len(FLAG) % 16) + b"}"
master_key = urandom(16)
flag_key = sha512(master_key).digest()
enc_flag = strxor(FLAG, flag_key[: len(FLAG)])

plaintext = urandom(16)
plain_state = bytes2matrix(plaintext)
cipher_state = copy.deepcopy(plain_state)
key_matrices = expand_key(master_key, 1)

add_round_key(cipher_state, key_matrices[0])
sub_bytes(cipher_state)
shift_rows(cipher_state)
mix_columns(cipher_state)
add_round_key(cipher_state, key_matrices[1])

im_cipher_state = copy.deepcopy(cipher_state)
inv_mix_columns(im_cipher_state)

rkp0 = copy.deepcopy(key_matrices[0])
rkp0_im = copy.deepcopy(rkp0)
inv_mix_columns(rkp0_im)

rkp1 = copy.deepcopy(key_matrices[1])
rkp1_im = copy.deepcopy(rkp1)
inv_mix_columns(rkp1_im)

print(f"{rkp0 = }")
print(f"{rkp0_im = }")
print(f"{rkp1 = }")
print(f"{rkp1_im = }")
print(f"{cipher_state = }")
print(f"{im_cipher_state = }")
print()


def check_equal_array(a, b):
    for x, y in zip(a, b):
        if x != y:
            return False
    return True


def encrypt(m, k):
    key_matrices = expand_key(k, 1)

    add_round_key(m, key_matrices[0])
    sub_bytes(m)
    shift_rows(m)
    mix_columns(m)
    add_round_key(m, key_matrices[1])

    return m


def combine_KP_w():
    if None in K[-1] and None in KP_im[0]:
        return True

    W = copy.deepcopy(K[-1])
    W.append(W.pop(0))
    for i in range(4):
        W[i] = s_box[W[i]] ^ [1, 0, 0, 0][i] if W[i] != None else None

    if None not in KP[0]:
        kp = copy.deepcopy(KP[0])
        for i, w in enumerate(W):
            if w != None:
                r = kp[i] ^ w
                if K[0][i] != None:
                    if K[0][i] != r:
                        print(
                            f"KP[0][{i}] ^ w[{i}] -> K[0][{i}]", r, K[0][i]
                        ) if DEBUG else None
                        return False
                else:
                    K[0][i] = r
                    if not forward(i, 0):
                        return False

    elif None not in W:
        w = copy.deepcopy(W)
        inv_mix_single_column(w)
        for i, kp in enumerate(KP_im[0]):
            if kp != None:
                r = w[i] ^ kp
                if K_im[0][i] != None and K_im[0][i] != r:
                    print(
                        f"w[{i}] ^ KP_im[0][{i}] -> K_im[0][{i}]", r, K_im[0][i]
                    ) if DEBUG else None
                    return False
                K_im[0][i] = r

    return True


def check_n_combine_KP():
    if not combine_KP_w():
        print("combine_KP_w issue") if DEBUG else None
        return False

    for i, w in enumerate(KP_im[:-1]):
        i += 1
        W = copy.deepcopy(w)

        for j, (kp, w) in enumerate(zip(KP_im[i], W)):
            if w != None and kp != None:
                r = kp ^ w
                if K_im[i][j] != None:
                    if K_im[i][j] != r:
                        print(
                            f"KP_im[{i - 1}][{j}] ^ KP_im[{i}][{j}] -> K_im[{i}][{j}]",
                            r,
                            K_im[i][j],
                        ) if DEBUG else None
                        return False
                else:
                    K_im[i][j] = r

        if None not in K_im[i]:
            K_temp = copy.deepcopy(K_im[i])
            mix_single_column(K_temp)
            for j, k_t in enumerate(K_temp):
                if K[i][j] != None:
                    if K[i][j] != k_t:
                        print(
                            f"K_im[{i}][{j}] != K[{i}][{j}]", k_t, K[i][j]
                        ) if DEBUG else None
                        return False
                else:
                    K[i][j] = k_t
                    # assert k_t == rkp0[i][j]
                    if not forward(j, i):
                        return False

    return True


def combine_K_KP_w():
    if all(
        [K[0][i] == None or (K[-1][i] == None and KP[0][i] == None) for i in range(4)]
    ):
        return True

    W = copy.deepcopy(K[-1])
    W.append(W.pop(0))
    for i in range(4):
        W[i] = s_box[W[i]] ^ [1, 0, 0, 0][i] if W[i] != None else None
    L = copy.deepcopy(W)
    R = copy.deepcopy(KP[0])

    for i, (l, r) in enumerate(zip(L, R)):
        if K[0][i] == None:
            continue
        if l == None and r != None:
            res = inv_s_box[r ^ K[0][i] ^ [1, 0, 0, 0][i]]
            if K[3][i - 3] != None:
                if K[3][i - 3] != res:
                    print(
                        f"KP[0][{i}] ^ K[0][{i}] -> K[3][{i} - 3]", res, K[3][i - 3]
                    ) if DEBUG else None
                    return False
            else:
                K[3][i - 3] = res
                if not forward(i - 3, 3):
                    return False
        elif r == None and l != None:
            res = K[0][i] ^ l
            if KP[0][i] != None and KP[0][i] != res:
                print(f"w[{i}] - 3] ^ K[0][{i}] -> KP[0][{i}]", res, K[3][i - 3])
                return False
            KP[0][i] = res
        elif r != None and l != None and r ^ l != K[0][i]:
            print(
                f"KP[0][{i}] ^ w[{i}] != K[0][{i}]", r ^ l, K[0][i]
            ) if DEBUG else None
            return False

    return True


def check_n_combine_K_KP():
    if not combine_K_KP_w():
        print("combine_K_KP_w issue") if DEBUG else None
        return False

    for i, k in enumerate(K[1:]):
        i += 1
        L = copy.deepcopy(KP[i - 1])
        R = copy.deepcopy(KP[i])

        for j, (l, r) in enumerate(zip(L, R)):
            if k[j] == None:
                continue
            if l == None and r != None:
                res = k[j] ^ r
                if KP[i - 1][j] != None and KP[i - 1][j] != res:
                    print(
                        f"K[{i}][{j}] ^ KP[{i}][{j}] -> KP[{i - 1}][{j}]",
                        res,
                        KP[i][j],
                    ) if DEBUG else None
                    return False
                KP[i - 1][j] = res
                # assert res == rkp1[i - 1][j]
            elif r == None and l != None:
                res = k[j] ^ l
                if KP[i][j] != None and KP[i][j] != res:
                    print(
                        f"K[{i}][{j}] ^ KP[{i - 1}][{j}] -> KP[{i}][{j}]",
                        res,
                        KP[i][j],
                    ) if DEBUG else None
                    return False
                KP[i][j] = res
                # assert res == rkp1[i][j]
            elif r != None and l != None and r ^ l != k[j]:
                return False

    for i, k in enumerate(K_im[1:]):
        i += 1
        L = copy.deepcopy(KP_im[i - 1])
        R = copy.deepcopy(KP_im[i])

        for j, (l, r) in enumerate(zip(L, R)):
            if k[j] == None:
                continue
            if l == None and r != None:
                res = k[j] ^ r
                if KP_im[i - 1][j] != None:
                    if KP_im[i - 1][j] != res:
                        print(
                            f"K_im[{i}][{j}] ^ KP_im[{i}][{j}] -> KP_im[{i - 1}][{j}]",
                            res,
                            KP_im[i][j],
                        ) if DEBUG else None
                        return False
                else:
                    KP_im[i - 1][j] = res
                    if not backward(j, i - 1):
                        return False
            elif r == None and l != None:
                res = k[j] ^ l
                if KP_im[i][j] != None:
                    if KP_im[i][j] != res:
                        print(
                            f"K_im[{i}][{j}] ^ KP_im[{i - 1}][{j}] -> KP_im[{i}][{j}]",
                            res,
                            KP_im[i][j],
                        ) if DEBUG else None
                        return False
                else:
                    KP_im[i][j] = res
                    if not backward(j, i):
                        return False
            elif r != None and l != None and r ^ l != k[j]:
                return False

    return True


def check_n_combine():
    res = True
    if not check_n_combine_KP():
        print("check_n_combine_KP issue") if DEBUG else None
        res = False
    if res and not check_n_combine_K_KP():
        print("check_n_combine_K_KP issue") if DEBUG else None
        res = False
    return res


def convert_K_n_KP():
    for i in range(4):
        if not None in K[i]:
            temp = copy.deepcopy(K[i])
            inv_mix_single_column(temp)
            for j in range(4):
                if K_im[i][j] != None and K_im[i][j] != temp[j]:
                    print(
                        f"K[{i}][{j}] -> K_im[{i}][{j}]", K_im[i][j], temp[j]
                    ) if DEBUG else None
                    return False
                K_im[i][j] = temp[j]
        if not None in K_im[i]:
            temp = copy.deepcopy(K_im[i])
            mix_single_column(temp)
            for j in range(4):
                if K[i][j] != None:
                    if K[i][j] != temp[j]:
                        print(
                            f"K_im[{i}][{j}] -> K[{i}][{j}]", K[i][j], temp[j]
                        ) if DEBUG else None
                        return False
                else:
                    K[i][j] = temp[j]
                    if not forward(j, i):
                        return False
        if not None in KP[i]:
            temp = copy.deepcopy(KP[i])
            inv_mix_single_column(temp)
            for j in range(4):
                if KP_im[i][j] != None:
                    if KP_im[i][j] != temp[j]:
                        print(
                            f"KP[{i}][{j}] -> KP_im[{i}][{j}]", KP_im[i][j], temp[j]
                        ) if DEBUG else None
                        return False
                else:
                    KP_im[i][j] = temp[j]
                    if not backward(j, i):
                        return False
        if not None in KP_im[i]:
            temp = copy.deepcopy(KP_im[i])
            mix_single_column(temp)
            for j in range(4):
                if KP[i][j] != None and KP[i][j] != temp[j]:
                    print(
                        f"KP_im[{i}][{j}] -> KP[{i}][{j}]", KP[i][j], temp[j]
                    ) if DEBUG else None
                    return False
                KP[i][j] = temp[j]
    return True


def backward(x, y):
    K[(y + x) % 4][x] = inv_s_box[C_im[y][x] ^ KP_im[y][x]] ^ P[(y + x) % 4][x]
    if not convert_K_n_KP():
        print("backward convert issue") if DEBUG else None
        return False
    return check_n_combine()


def forward(x, y):
    KP_im[(y - x) % 4][x] = s_box[P[y][x] ^ K[y][x]] ^ C_im[(y - x) % 4][x]
    if not convert_K_n_KP():
        print("forward convert issue") if DEBUG else None
        return False
    return check_n_combine()


K_checkpoint = []
K_im_checkpoint = []
KP_checkpoint = []
KP_im_checkpoint = []


def set_checkpoint(state):
    global K_checkpoint, K_im_checkpoint, KP_checkpoint, KP_im_checkpoint
    if state >= len(K_checkpoint):
        K_checkpoint.append([])
        K_im_checkpoint.append([])
        KP_checkpoint.append([])
        KP_im_checkpoint.append([])
        assert state == len(K_checkpoint) - 1
    K_checkpoint[state] = copy.deepcopy(K)
    K_im_checkpoint[state] = copy.deepcopy(K_im)
    KP_checkpoint[state] = copy.deepcopy(KP)
    KP_im_checkpoint[state] = copy.deepcopy(KP_im)


def restore_checkpoint(state):
    global K, K_im, KP, KP_im
    K = copy.deepcopy(K_checkpoint[state])
    K_im = copy.deepcopy(K_im_checkpoint[state])
    KP = copy.deepcopy(KP_checkpoint[state])
    KP_im = copy.deepcopy(KP_im_checkpoint[state])


class Bruteforcer:
    V = []
    T = []
    X = []
    Y = []
    RESULT = []

    def add(self, *var):
        v = []
        t = []
        x = []
        y = []

        def recursive(var):
            for v_ in var:
                if isinstance(v_, list):
                    recursive(v_)
                else:
                    v.append(v_)

        recursive(var)

        for i in range(len(v)):
            _v = v[i].split("_")
            assert len(_v) in [3, 4]
            assert _v[0] in ["K", "KP"]
            v[i] = _v[0]
            if len(_v) == 4:
                assert _v[1] == "im"
                t.append(1)
                v[i] += "_im"
            else:
                t.append(0)
            x.append(int(_v[len(_v) - 1]))
            y.append(int(_v[len(_v) - 2]))

        self.V.append(v)
        self.T.append(t)
        self.X.append(x)
        self.Y.append(y)

    def run(self, is_test=False):
        print(f"{self.V = }")
        print(f"{self.T = }")
        print(f"{self.X = }")
        print(f"{self.Y = }")

        def run_recursive(i=0):
            if i >= len(self.V):
                if is_test or all([None not in x for x in K]):
                    print(f"{K = }")
                    print(f"{K_im = }")
                    print(f"{KP = }")
                    print(f"{KP_im = }")
                    print()
                    self.RESULT.append(copy.deepcopy(K))
                return
            set_checkpoint(i)
            v = self.V[i]
            t = self.T[i]
            x = self.X[i]
            y = self.Y[i]
            possiblity = []

            def recursive(data=[], j=0):
                if j >= len(v):
                    possiblity.append(copy.deepcopy(data))
                    return
                for val in range(0xFF):
                    for k in range(j):
                        eval(v[k])[y[k]][x[k]] = data[k]
                        if t[k] == 0:
                            forward(x[k], y[k])
                        else:
                            backward(x[k], y[k])
                    if eval(v[j])[y[j]][x[j]] != None and eval(v[j])[y[j]][x[j]] != val:
                        restore_checkpoint(i)
                        continue
                    eval(v[j])[y[j]][x[j]] = val
                    if t[j] == 0:
                        if not forward(x[j], y[j]):
                            restore_checkpoint(i)
                            continue
                    else:
                        if not backward(x[j], y[j]):
                            restore_checkpoint(i)
                            continue
                    recursive(data + [val], j + 1)
                    restore_checkpoint(i)

            recursive()
            if len(possiblity) == 0:
                restore_checkpoint(i)
                return
            elif len(possiblity) < 20:
                print(f"{possiblity = }")
            else:
                print("possibility =", len(possiblity))

            assert [rkp1_im[0][1], rkp1_im[0][2]] in possiblity

            for p in tqdm(possiblity):
                for k in range(len(p)):
                    eval(v[k])[y[k]][x[k]] = p[k]
                    if t[k] == 0:
                        forward(x[k], y[k])
                    else:
                        backward(x[k], y[k])

                run_recursive(i + 1)

                restore_checkpoint(i)
            restore_checkpoint(i)

        run_recursive()


DEBUG = True

K = [[None] * 4 for _ in range(4)]
K_im = [[None] * 4 for _ in range(4)]
KP = [[None] * 4 for _ in range(4)]
KP_im = [[None] * 4 for _ in range(4)]

P, C = plain_state, cipher_state

C_im = copy.deepcopy(C)
inv_mix_columns(C_im)

K[0][0] = rkp0[0][0]
K[3][2] = rkp0[3][2]
K[3][3] = rkp0[3][3]
forward(0, 0)
forward(2, 3)
forward(3, 3)

KP_im[0][1] = rkp0_im[0][1]
KP_im[0][2] = rkp0_im[0][2]
backward(1, 0)
backward(2, 0)

brute = Bruteforcer()
# brute.add("KP_im_0_1", "KP_im_0_2")
brute.add("KP_im_1_3", "KP_im_2_3")
brute.run(True)
