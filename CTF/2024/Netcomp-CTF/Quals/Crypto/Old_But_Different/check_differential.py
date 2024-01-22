import copy
from os import urandom

from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import xor

org_hex = hex


def hex(x: int, width=4):
    res = org_hex(x)[2:]
    return "0x" + res.rjust((width - len(res)) % width + len(res), "0")


def hex_array(array: list):
    return [hex(x) for x in array]


left_half = lambda t: t >> 32 & 0xFFFFFFFF
right_half = lambda t: t & 0xFFFFFFFF


class DifferentialAnalysis:
    def __init__(
        self,
        num_plain: int = 12,
        with_key=True,
        with_random_plain=True,
    ):
        self.num_plain = num_plain if with_random_plain else 1
        self.keys = (
            [bytes_to_long(urandom(4)) for _ in range(4)] if with_key else [0] * 4
        )
        self.with_random_plain = with_random_plain

        self.trace = [[[], []] for _ in range(self.num_plain)]

        self.addition = [dict() for _ in range(self.num_plain)]

    def set_choosen_plaintext(self, differential):
        self.p = []
        self.p_diff = []
        self.c = []
        self.c_diff = []
        self.ptr = 0
        self.ptr_flag = 0
        for i in range(self.num_plain):
            r_plain = bytes_to_long(urandom(8)) if self.with_random_plain else 0
            self.p.append(r_plain)
            self.c.append(self.cipher(self.p[i]))
            self.p_diff.append(self.p[i] ^ differential)
            self.ptr_flag = 1
            self.c_diff.append(self.cipher(self.p_diff[i]))
            self.ptr += 1
            self.ptr_flag = 0

    def split(self, t: int):
        return left_half(t), right_half(t)

    def combine(self, left: int, right: int):
        return (left << 32) | (right)

    def set_trace(self, left, right, ks=0):
        self.trace[self.ptr][self.ptr_flag].append((left, right, ks))

    def h(self, x, n):
        return (x >> (n * 8)) & 0xFF

    def swap(self, x):
        return ((x << 4) | (x >> 4)) & 0xFF

    def g(self, x, y, z):
        res = (3 * x + 5 * y + 7 * z) % 0x100
        return self.swap(res)

    def f(self, x):
        x0 = self.h(x, 0)
        x1 = self.h(x, 1)
        x2 = self.h(x, 2)
        x3 = self.h(x, 3)

        _x0 = self.g(x0, x1, 0)
        _x1 = self.g(x2, x1 ^ _x0, 1)
        _x2 = self.g(x2 ^ _x1, x3, 0)
        _x3 = self.g(x3, x3, 1)

        return (_x3 << 24) | (_x2 << 16) | (_x1 << 8) | _x0

    def cipher(self, pt):
        left, right = self.split(pt)

        left, right = left, right ^ left
        num_round = 4
        for i in range(num_round):
            ks = self.f(right ^ self.keys[i])
            self.set_trace(left, right, ks)
            left, right = left ^ ks, right
            if i == num_round - 1:
                break
            left, right = right, left
        self.set_trace(left, right)

        left, right = left, right ^ left

        assert left < 2**32
        assert right < 2**32
        return self.combine(left, right)

    def print_res(self, differential, output_differential):
        MAX_COLL = 1
        NUM_CHAR_PER_COLL = 120
        NUM_LINE = 12 + len(self.addition[0].items())
        print(
            "diff =",
            hex(differential),
            "\toutput_diff =",
            hex(output_differential),
            "\tHas Keys:",
            [hex(key) for key in self.keys],
        )
        for i in range((self.num_plain - 1) // MAX_COLL + 1):
            array_string = ["" for _ in range(NUM_LINE)]
            for j in range(MAX_COLL):
                if MAX_COLL * i + j >= self.num_plain:
                    break
                idx = MAX_COLL * i + j
                array_string[0] += (
                    f"#[{idx + 1}]"
                    + "-"
                    * (
                        (NUM_CHAR_PER_COLL * (j + 1))
                        - 3
                        - ((idx + 1) // 10 + 1)
                        - len(array_string[0])
                        - 1
                    )
                    + " "
                )
                for k, l in enumerate(range(1, 1 + 5)):
                    array_string[
                        l
                    ] += f"{k + 1}: {hex(self.trace[idx][0][k][0], 8)} {hex(self.trace[idx][0][k][1], 8)} | {hex(self.trace[idx][0][k][2], 8)} -> {hex(self.trace[idx][0][k][0] ^ self.trace[idx][1][k][0], 8)} {hex(self.trace[idx][0][k][1] ^ self.trace[idx][1][k][1], 8)} | {hex(self.trace[idx][0][k][2] ^ self.trace[idx][1][k][2], 8)} <- {hex(self.trace[idx][1][k][0], 8)} {hex(self.trace[idx][1][k][1], 8)} | {hex(self.trace[idx][1][k][2], 8)}"
                    array_string[l] += " " * (
                        (NUM_CHAR_PER_COLL * (j + 1)) - len(array_string[l])
                    )
                array_string[6] += (
                    "-" * (NUM_CHAR_PER_COLL * (j + 1) - len(array_string[6]) - 1) + " "
                )
                array_string[7] += f"res  = {hex(self.c[idx])}"
                array_string[7] += " " * (
                    (NUM_CHAR_PER_COLL * (j + 1)) - len(array_string[7])
                )
                array_string[8] += f"_res = {hex(self.c_diff[idx])}"
                array_string[8] += " " * (
                    (NUM_CHAR_PER_COLL * (j + 1)) - len(array_string[8])
                )
                array_string[9] += f"diff = {hex(self.c_diff[idx] ^ self.c[idx])}"
                array_string[9] += " " * (
                    (NUM_CHAR_PER_COLL * (j + 1)) - len(array_string[9])
                )
                for k, a in enumerate(self.addition[idx]):
                    array_string[10 + k] += f"{a} = {self.addition[idx][a]}"
                    array_string[10 + k] += " " * (
                        (NUM_CHAR_PER_COLL * (j + 1)) - len(array_string[10 + k])
                    )
            for arr_string in array_string:
                print(arr_string)

    def reverse_final_operation(self):
        for i in range(self.num_plain):
            c_left, c_right = self.split(self.c[i])
            c_right ^= c_left
            c_diff_left, c_diff_right = self.split(self.c_diff[i])
            c_diff_right ^= c_diff_left

            self.c[i] = self.combine(c_left, c_right)
            self.c_diff[i] = self.combine(c_diff_left, c_diff_right)

    def reverse_last_operation(self, key):
        for i in range(self.num_plain):
            c_left, c_right = self.split(self.c[i])
            c_diff_left, c_diff_right = self.split(self.c_diff[i])

            c_left ^= self.f(c_right ^ key)
            c_diff_left ^= self.f(c_diff_right ^ key)

            c_left, c_right = c_right, c_left
            c_diff_left, c_diff_right = c_diff_right, c_diff_left

            self.c[i] = self.combine(c_left, c_right)
            self.c_diff[i] = self.combine(c_diff_left, c_diff_right)

    def crack_key(self, o_diff, comparison, key_range=None, offset=0, list_key=None):
        list_key = list_key or [0]
        key_range = key_range or 0x100000000
        offset *= 8

        o_diff &= comparison

        res = []
        for k in list_key:
            for _k in range(key_range):
                key = k | (_k << offset)
                counter = 0
                for i in range(self.num_plain):
                    c_left, c_right = self.split(self.c[i])
                    c_diff_left, c_diff_right = self.split(self.c_diff[i])

                    f_out = c_left ^ self.f(c_right ^ key)
                    f_diff_out = c_diff_left ^ self.f(c_diff_right ^ key)

                    f_diff = f_diff_out ^ f_out
                    if f_diff & comparison != o_diff:
                        break
                    counter += 1

                if counter == self.num_plain and key not in res:
                    res.append(key)
                    yield key

    def crack_last_key(self, comparison, key_range=None, offset=0, list_key=None):
        list_key = list_key or [0]
        key_range = key_range or 0x100000000
        offset *= 8

        res = []
        for k in list_key:
            for _k in range(key_range):
                key = k | (_k << offset)
                counter = 0
                for i in range(self.num_plain):
                    c_left, c_right = self.split(self.c[i])
                    p_left, _ = self.split(self.p[i])
                    c_diff_left, c_diff_right = self.split(self.c_diff[i])
                    p_diff_left, _ = self.split(self.p_diff[i])

                    f_out = c_left ^ self.f(c_right ^ key)
                    f_diff_out = c_diff_left ^ self.f(c_diff_right ^ key)

                    if (
                        f_out & comparison != p_left & comparison
                        or f_diff_out & comparison != p_diff_left & comparison
                    ):
                        break
                    counter += 1

                if counter == self.num_plain and key not in res:
                    res.append(key)
                    yield key

    def main(self):
        diff1 = 0x0080808000808080
        diff2 = 0x0000000000808080
        diff3 = 0x0000000000080000
        diff4 = 0x0000000000080808
        out_diff = 0x00080000

        keys = []
        # Crack Round 4
        self.set_choosen_plaintext(diff1)
        self.reverse_final_operation()

        key3 = self.crack_key(out_diff, 0xFF, 0x10000)
        key3 = self.crack_key(out_diff, 0xFFFFFFFF, 0x10000, 2, key3)
        # End Crack Round 4
        for k3 in list(key3):
            # Crack Round 3
            self.set_choosen_plaintext(diff2)
            self.reverse_final_operation()
            self.reverse_last_operation(k3)

            key2 = self.crack_key(out_diff, 0xFF, 0x10000)
            key2 = self.crack_key(out_diff, 0xFFFFFFFF, 0x10000, 2, key2)
            # End Crack Round 3

            for k2 in list(key2):
                # Crack Round 2
                self.set_choosen_plaintext(diff3)
                self.reverse_final_operation()
                self.reverse_last_operation(k3)
                self.reverse_last_operation(k2)

                key1 = self.crack_key(out_diff, 0xFF, 0x10000)
                key1 = self.crack_key(out_diff, 0xFFFFFFFF, 0x10000, 2, key1)
                # End Crack Round 2

                for k1 in list(key1):
                    # Crack Round 1
                    self.set_choosen_plaintext(diff4)
                    self.reverse_final_operation()
                    self.reverse_last_operation(k3)
                    self.reverse_last_operation(k2)
                    self.reverse_last_operation(k1)

                    key0 = self.crack_last_key(0xFF, 0x10000)
                    key0 = self.crack_last_key(0xFFFFFFFF, 0x10000, 2, key0)
                    # End Crack Round 1

                    for k0 in key0:
                        keys.append([hex(k0), hex(k1), hex(k2), hex(k3)])

        print("org_keys =", hex_array(self.keys))
        print(f"{keys = }")


DifferentialAnalysis().main()
