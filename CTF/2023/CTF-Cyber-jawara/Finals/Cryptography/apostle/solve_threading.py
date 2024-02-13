import copy
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import reduce
from hashlib import sha512
from os import urandom

from aes import *
from Crypto.Util.strxor import strxor
from tqdm import tqdm


def xor(*args):
    return [reduce(lambda x, y: x ^ y, v) for v in zip(*args)]


while True:
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
    if (
        rkp1_im[0][1] % 2 == 0
        and rkp1_im[0][2] % 2 == 0
        and rkp1_im[1][3] % 2 == 0
        and rkp1_im[2][3] % 2 == 0
    ):
        continue
    break

print(f"{rkp0 = }")
print(f"{rkp0_im = }")
print(f"{rkp1 = }")
print(f"{rkp1_im = }")
print(f"{cipher_state = }")
print(f"{im_cipher_state = }")
print()


class Attack:
    def __init__(self):
        self.K = [[None] * 4 for _ in range(4)]
        self.K_im = [[None] * 4 for _ in range(4)]
        self.KP = [[None] * 4 for _ in range(4)]
        self.KP_im = [[None] * 4 for _ in range(4)]

        self.K_checkpoint = []
        self.K_im_checkpoint = []
        self.KP_checkpoint = []
        self.KP_im_checkpoint = []

        self.DEBUG = False

    def combine_KP_w(self):
        if None in self.K[-1] and None in self.KP_im[0]:
            return True

        W = copy.deepcopy(self.K[-1])
        W.append(W.pop(0))
        for i in range(4):
            W[i] = s_box[W[i]] ^ [1, 0, 0, 0][i] if W[i] != None else None

        if None not in self.KP[0]:
            kp = copy.deepcopy(self.KP[0])
            for i, w in enumerate(W):
                if w != None:
                    r = kp[i] ^ w
                    if self.K[0][i] != None:
                        if self.K[0][i] != r:
                            (
                                print(
                                    f"KP[0][{i}] ^ w[{i}] -> K[0][{i}]", r, self.K[0][i]
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.K[0][i] = r
                        if not self.forward(i, 0):
                            return False

        elif None not in W:
            w = copy.deepcopy(W)
            inv_mix_single_column(w)
            for i, kp in enumerate(self.KP_im[0]):
                if kp != None:
                    r = w[i] ^ kp
                    if self.K_im[0][i] != None and self.K_im[0][i] != r:
                        (
                            print(
                                f"w[{i}] ^ KP_im[0][{i}] -> K_im[0][{i}]",
                                r,
                                self.K_im[0][i],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                    self.K_im[0][i] = r

        return True

    def check_n_combine_KP(self):
        if not self.combine_KP_w():
            print("combine_KP_w issue") if self.DEBUG else None
            return False

        for i, w in enumerate(self.KP_im[:-1]):
            i += 1
            W = copy.deepcopy(w)

            for j, (kp, w) in enumerate(zip(self.KP_im[i], W)):
                if w != None and kp != None:
                    r = kp ^ w
                    if self.K_im[i][j] != None:
                        if self.K_im[i][j] != r:
                            (
                                print(
                                    f"KP_im[{i - 1}][{j}] ^ KP_im[{i}][{j}] -> K_im[{i}][{j}]",
                                    r,
                                    self.K_im[i][j],
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.K_im[i][j] = r

            if None not in self.K_im[i]:
                K_temp = copy.deepcopy(self.K_im[i])
                mix_single_column(K_temp)
                for j, k_t in enumerate(K_temp):
                    if self.K[i][j] != None:
                        if self.K[i][j] != k_t:
                            (
                                print(
                                    f"K_im[{i}][{j}] != K[{i}][{j}]", k_t, self.K[i][j]
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.K[i][j] = k_t
                        # assert k_t == rkp0[i][j]
                        if not self.forward(j, i):
                            return False

        return True

    def combine_K_KP_w(self):
        if all(
            [
                self.K[0][i] == None
                or (self.K[-1][i] == None and self.KP[0][i] == None)
                for i in range(4)
            ]
        ):
            return True

        W = copy.deepcopy(self.K[-1])
        W.append(W.pop(0))
        for i in range(4):
            W[i] = s_box[W[i]] ^ [1, 0, 0, 0][i] if W[i] != None else None
        L = copy.deepcopy(W)
        R = copy.deepcopy(self.KP[0])

        for i, (l, r) in enumerate(zip(L, R)):
            if self.K[0][i] == None:
                continue
            if l == None and r != None:
                res = inv_s_box[r ^ self.K[0][i] ^ [1, 0, 0, 0][i]]
                if self.K[3][i - 3] != None:
                    if self.K[3][i - 3] != res:
                        (
                            print(
                                f"KP[0][{i}] ^ K[0][{i}] -> K[3][{i} - 3]",
                                res,
                                self.K[3][i - 3],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                else:
                    self.K[3][i - 3] = res
                    if not self.forward(i - 3, 3):
                        return False
            elif r == None and l != None:
                res = self.K[0][i] ^ l
                if self.KP[0][i] != None and self.KP[0][i] != res:
                    print(
                        f"w[{i}] - 3] ^ K[0][{i}] -> KP[0][{i}]", res, self.K[3][i - 3]
                    )
                    return False
                self.KP[0][i] = res
            elif r != None and l != None and r ^ l != self.K[0][i]:
                (
                    print(f"KP[0][{i}] ^ w[{i}] != K[0][{i}]", r ^ l, self.K[0][i])
                    if self.DEBUG
                    else None
                )
                return False

        return True

    def check_n_combine_K_KP(self):
        if not self.combine_K_KP_w():
            print("combine_K_KP_w issue") if self.DEBUG else None
            return False

        for i, k in enumerate(self.K[1:]):
            i += 1
            L = copy.deepcopy(self.KP[i - 1])
            R = copy.deepcopy(self.KP[i])

            for j, (l, r) in enumerate(zip(L, R)):
                if k[j] == None:
                    continue
                if l == None and r != None:
                    res = k[j] ^ r
                    if self.KP[i - 1][j] != None and self.KP[i - 1][j] != res:
                        (
                            print(
                                f"K[{i}][{j}] ^ KP[{i}][{j}] -> KP[{i - 1}][{j}]",
                                res,
                                self.KP[i][j],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                    self.KP[i - 1][j] = res
                    # assert res == rkp1[i - 1][j]
                elif r == None and l != None:
                    res = k[j] ^ l
                    if self.KP[i][j] != None and self.KP[i][j] != res:
                        (
                            print(
                                f"K[{i}][{j}] ^ KP[{i - 1}][{j}] -> KP[{i}][{j}]",
                                res,
                                self.KP[i][j],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                    self.KP[i][j] = res
                    # assert res == rkp1[i][j]
                elif r != None and l != None and r ^ l != k[j]:
                    return False

        for i, k in enumerate(self.K_im[1:]):
            i += 1
            L = copy.deepcopy(self.KP_im[i - 1])
            R = copy.deepcopy(self.KP_im[i])

            for j, (l, r) in enumerate(zip(L, R)):
                if k[j] == None:
                    continue
                if l == None and r != None:
                    res = k[j] ^ r
                    if self.KP_im[i - 1][j] != None:
                        if self.KP_im[i - 1][j] != res:
                            (
                                print(
                                    f"K_im[{i}][{j}] ^ KP_im[{i}][{j}] -> KP_im[{i - 1}][{j}]",
                                    res,
                                    self.KP_im[i][j],
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.KP_im[i - 1][j] = res
                        if not self.backward(j, i - 1):
                            return False
                elif r == None and l != None:
                    res = k[j] ^ l
                    if self.KP_im[i][j] != None:
                        if self.KP_im[i][j] != res:
                            (
                                print(
                                    f"K_im[{i}][{j}] ^ KP_im[{i - 1}][{j}] -> KP_im[{i}][{j}]",
                                    res,
                                    self.KP_im[i][j],
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.KP_im[i][j] = res
                        if not self.backward(j, i):
                            return False
                elif r != None and l != None and r ^ l != k[j]:
                    return False

        return True

    def check_n_combine(self):
        res = True
        if not self.check_n_combine_KP():
            print("check_n_combine_KP issue") if self.DEBUG else None
            res = False
        if res and not self.check_n_combine_K_KP():
            print("check_n_combine_K_KP issue") if self.DEBUG else None
            res = False
        return res

    def convert_K_n_KP(self):
        for i in range(4):
            if not None in self.K[i]:
                temp = copy.deepcopy(self.K[i])
                inv_mix_single_column(temp)
                for j in range(4):
                    if self.K_im[i][j] != None and self.K_im[i][j] != temp[j]:
                        (
                            print(
                                f"K[{i}][{j}] -> K_im[{i}][{j}]",
                                self.K_im[i][j],
                                temp[j],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                    self.K_im[i][j] = temp[j]
            if not None in self.K_im[i]:
                temp = copy.deepcopy(self.K_im[i])
                mix_single_column(temp)
                for j in range(4):
                    if self.K[i][j] != None:
                        if self.K[i][j] != temp[j]:
                            (
                                print(
                                    f"K_im[{i}][{j}] -> K[{i}][{j}]",
                                    self.K[i][j],
                                    temp[j],
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.K[i][j] = temp[j]
                        if not self.forward(j, i):
                            return False
            if not None in self.KP[i]:
                temp = copy.deepcopy(self.KP[i])
                inv_mix_single_column(temp)
                for j in range(4):
                    if self.KP_im[i][j] != None:
                        if self.KP_im[i][j] != temp[j]:
                            (
                                print(
                                    f"KP[{i}][{j}] -> KP_im[{i}][{j}]",
                                    self.KP_im[i][j],
                                    temp[j],
                                )
                                if self.DEBUG
                                else None
                            )
                            return False
                    else:
                        self.KP_im[i][j] = temp[j]
                        if not self.backward(j, i):
                            return False
            if not None in self.KP_im[i]:
                temp = copy.deepcopy(self.KP_im[i])
                mix_single_column(temp)
                for j in range(4):
                    if self.KP[i][j] != None and self.KP[i][j] != temp[j]:
                        (
                            print(
                                f"KP_im[{i}][{j}] -> KP[{i}][{j}]",
                                self.KP[i][j],
                                temp[j],
                            )
                            if self.DEBUG
                            else None
                        )
                        return False
                    self.KP[i][j] = temp[j]
        return True

    def backward(self, x, y):
        self.K[(y + x) % 4][x] = (
            inv_s_box[C_im[y][x] ^ self.KP_im[y][x]] ^ P[(y + x) % 4][x]
        )
        if not self.convert_K_n_KP():
            print("backward convert issue") if self.DEBUG else None
            return False
        return self.check_n_combine()

    def forward(self, x, y):
        self.KP_im[(y - x) % 4][x] = (
            s_box[P[y][x] ^ self.K[y][x]] ^ C_im[(y - x) % 4][x]
        )
        if not self.convert_K_n_KP():
            print("forward convert issue") if self.DEBUG else None
            return False
        return self.check_n_combine()

    def set_checkpoint(self, state):
        if state >= len(self.K_checkpoint):
            self.K_checkpoint.append([])
            self.K_im_checkpoint.append([])
            self.KP_checkpoint.append([])
            self.KP_im_checkpoint.append([])
            assert state == len(self.K_checkpoint) - 1
        self.K_checkpoint[state] = copy.deepcopy(self.K)
        self.K_im_checkpoint[state] = copy.deepcopy(self.K_im)
        self.KP_checkpoint[state] = copy.deepcopy(self.KP)
        self.KP_im_checkpoint[state] = copy.deepcopy(self.KP_im)

    def restore_checkpoint(self, state):
        self.K = copy.deepcopy(self.K_checkpoint[state])
        self.K_im = copy.deepcopy(self.K_im_checkpoint[state])
        self.KP = copy.deepcopy(self.KP_checkpoint[state])
        self.KP_im = copy.deepcopy(self.KP_im_checkpoint[state])

    def get_bruteforcer(self):
        return Bruteforcer(self)


class ThreadLocalVars(Attack, threading.local):
    def __init__(self, attack: Attack):
        super().__init__()
        self.K = attack.K
        self.K_im = attack.K_im
        self.KP = attack.KP
        self.KP_im = attack.KP_im


class Bruteforcer:
    V = []
    T = []
    X = []
    Y = []
    RESULT = []

    def __init__(self, attack: Attack):
        self.thread_local_vars = ThreadLocalVars(attack)

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

        def run_recursive_parallel(i=0, state=None):
            thread_vars = self.thread_local_vars
            if state is not None:
                thread_vars.K = state["K"]
                thread_vars.K_im = state["K_im"]
                thread_vars.KP = state["KP"]
                thread_vars.KP_im = state["KP_im"]
                thread_vars.K_checkpoint = state["K_checkpoint"]
                thread_vars.K_im_checkpoint = state["K_im_checkpoint"]
                thread_vars.KP_checkpoint = state["KP_checkpoint"]
                thread_vars.KP_im_checkpoint = state["KP_im_checkpoint"]
                thread_vars.DEBUG = state["DEBUG"]

            if i >= len(self.V):
                if is_test or all([None not in x for x in thread_vars.K]):
                    print(f"{thread_vars.K = }")
                    print(f"{thread_vars.K_im = }")
                    print(f"{thread_vars.KP = }")
                    print(f"{thread_vars.KP_im = }")
                    print()
                    self.RESULT.append(copy.deepcopy(thread_vars.K))
                return

            thread_vars.set_checkpoint(i)
            v = self.V[i]
            t = self.T[i]
            x = self.X[i]
            y = self.Y[i]
            possiblity = []

            def recursive(data=[], j=0):
                if j >= len(v):
                    val = copy.deepcopy(data)
                    possiblity.append(val)
                    return
                for val in range(0xFF):
                    for k in range(j):
                        eval("thread_vars." + v[k])[y[k]][x[k]] = data[k]
                        if t[k] == 0:
                            thread_vars.forward(x[k], y[k])
                        else:
                            thread_vars.backward(x[k], y[k])
                    if (
                        eval("thread_vars." + v[j])[y[j]][x[j]] != None
                        and eval("thread_vars." + v[j])[y[j]][x[j]] != val
                    ):
                        thread_vars.restore_checkpoint(i)
                        continue
                    eval("thread_vars." + v[j])[y[j]][x[j]] = val
                    if t[j] == 0:
                        if not thread_vars.forward(x[j], y[j]):
                            thread_vars.restore_checkpoint(i)
                            continue
                    else:
                        if not thread_vars.backward(x[j], y[j]):
                            thread_vars.restore_checkpoint(i)
                            continue
                    recursive(data + [val], j + 1)
                    thread_vars.restore_checkpoint(i)

            recursive()

            if len(possiblity) == 0:
                thread_vars.restore_checkpoint(i)
                return
            elif len(possiblity) < 20:
                print(f"{possiblity = }")
            else:
                print("possibility =", len(possiblity))

            # assert [rkp1_im[0][1], rkp1_im[0][2]] in possiblity

            with ThreadPoolExecutor() as executor:
                futures = []
                for p in (pbar := tqdm(possiblity, total=len(possiblity))):
                    # pbar.set_description(f"Processing possibilities ~ {p}")
                    futures.append(
                        executor.submit(
                            process_possibility,
                            p,
                            v,
                            x,
                            y,
                            t,
                            i,
                            {
                                "K": copy.deepcopy(thread_vars.K),
                                "K_im": copy.deepcopy(thread_vars.K_im),
                                "KP": copy.deepcopy(thread_vars.KP),
                                "KP_im": copy.deepcopy(thread_vars.KP_im),
                                "K_checkpoint": copy.deepcopy(thread_vars.K_checkpoint),
                                "K_im_checkpoint": copy.deepcopy(
                                    thread_vars.K_im_checkpoint
                                ),
                                "KP_checkpoint": copy.deepcopy(
                                    thread_vars.KP_checkpoint
                                ),
                                "KP_im_checkpoint": copy.deepcopy(
                                    thread_vars.KP_im_checkpoint
                                ),
                                "DEBUG": thread_vars.DEBUG,
                            },
                        )
                    )

                for future in tqdm(
                    as_completed(futures),
                    total=len(possiblity),
                    desc="Processing possibilities",
                ):
                    future.result()

            thread_vars.restore_checkpoint(i)

        def process_possibility(p, v, x, y, t, i, current_state=None):
            thread_vars = self.thread_local_vars  # Get thread-local variables
            if current_state is not None:
                thread_vars.K = current_state["K"]
                thread_vars.K_im = current_state["K_im"]
                thread_vars.KP = current_state["KP"]
                thread_vars.KP_im = current_state["KP_im"]
                thread_vars.K_checkpoint = current_state["K_checkpoint"]
                thread_vars.K_im_checkpoint = current_state["K_im_checkpoint"]
                thread_vars.KP_checkpoint = current_state["KP_checkpoint"]
                thread_vars.KP_im_checkpoint = current_state["KP_im_checkpoint"]
                thread_vars.DEBUG = current_state["DEBUG"]

            thread_vars.set_checkpoint(i)

            # if (
            #     eval("thread_vars." + v[0])[y[0]][x[0]] == rkp1_im[0][1]
            #     and eval("thread_vars." + v[1])[y[1]][x[1]] == rkp1_im[0][2]
            # ):
            thread_vars.DEBUG = True

            for k in range(len(p)):
                eval("thread_vars." + v[k])[y[k]][x[k]] = p[k]
                if t[k] == 0:
                    thread_vars.forward(x[k], y[k])
                else:
                    thread_vars.backward(x[k], y[k])

            run_recursive_parallel(i + 1, current_state)

            thread_vars.restore_checkpoint(i)

        run_recursive_parallel()


# P = "230d0aa96b6d5233f851f8b13d63772d"
# C = "f4cb06ffeaa42a8f25b79c0e9bb18a0e"
# P, C = bytes.fromhex(P), bytes.fromhex(C)
# P, C = bytes2matrix(P), bytes2matrix(C)

P, C = plain_state, cipher_state

C_im = copy.deepcopy(C)
inv_mix_columns(C_im)


# K[0][0] = 8
# K[3][2] = 171
# K[3][3] = 236
# forward(0, 0)
# forward(2, 3)
# forward(3, 3)
attack = Attack()

attack.K[0][0] = rkp0[0][0]
attack.K[3][2] = rkp0[3][2]
attack.K[3][3] = rkp0[3][3]
attack.forward(0, 0)
attack.forward(2, 3)
attack.forward(3, 3)

attack.KP_im[0][1] = rkp1_im[0][1]
attack.backward(1, 0)
attack.KP_im[0][2] = rkp1_im[0][2]
attack.backward(2, 0)

brute = attack.get_bruteforcer()
# brute.add("KP_im_0_1", "KP_im_0_2")
brute.add("KP_im_1_3", "KP_im_2_3")
brute.run(True)
