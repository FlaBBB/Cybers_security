from os import urandom

from Crypto.Util.number import bytes_to_long, long_to_bytes

org_hex = hex


def hex(x: int, width=4):
    res = org_hex(x)[2:]
    return "0x" + res.rjust((width - len(res)) % width + len(res), "0")


def hex_array(array: list):
    return [hex(x) for x in array]


left_half = lambda t: t >> 32 & 0xFFFFFFFF
right_half = lambda t: t & 0xFFFFFFFF


class Exploit:
    def __init__(self, num_plain: int = 12):
        self.num_plain = num_plain
        self.keys = [bytes_to_long(urandom(4)) for _ in range(4)]

        self.flag = b"netcomp{f34l_w1th_d1ff3renT1al_Cr7pt4naLyS1s}"
        self.c_flag = self.encrypt(self.flag)

    def get_set_choosen(self, differential):
        p = []
        p_diff = []
        c = []
        c_diff = []
        for i in range(self.num_plain):
            r_plain = bytes_to_long(urandom(8))
            p.append(r_plain)
            c.append(bytes_to_long(self.encrypt(long_to_bytes(p[i]))[:8]))
            p_diff.append(p[i] ^ differential)
            c_diff.append(bytes_to_long(self.encrypt(long_to_bytes(p_diff[i]))[:8]))

        return (p, p_diff, c, c_diff)

    def split(self, t: int):
        return left_half(t), right_half(t)

    def combine(self, left: int, right: int):
        return (left << 32) | (right)

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

    def cipher(self, pt, keys):
        left, right = self.split(pt)

        left, right = left, right ^ left
        num_round = 4
        for i in range(num_round):
            left, right = left ^ self.f(right ^ keys[i]), right
            if i == num_round - 1:
                break
            left, right = right, left

        left, right = left, right ^ left

        assert left < 2**32
        assert right < 2**32
        return self.combine(left, right)

    def pad(self, msg):
        return msg + chr(8 - len(msg) % 8).encode() * (8 - len(msg) % 8)

    def encrypt(self, msg):
        encrypted = b""
        msg = self.pad(msg)
        for i in range(len(msg) // 8):
            encrypted += long_to_bytes(
                self.cipher(bytes_to_long(msg[8 * i : 8 * (i + 1)]), self.keys)
            )
        return encrypted

    def decrypt(self, msg, keys):
        decrypted = b""
        dec_keys = [keys[3], keys[2], keys[1], keys[0]]
        for i in range(len(msg) // 8):
            decrypted += long_to_bytes(
                self.cipher(bytes_to_long(msg[8 * i : 8 * (i + 1)]), dec_keys)
            )
        return decrypted

    def reverse_final_operation(self, _set):
        _, _, c, c_diff = _set
        for i in range(self.num_plain):
            c_left, c_right = self.split(c[i])
            c_right ^= c_left
            c_diff_left, c_diff_right = self.split(c_diff[i])
            c_diff_right ^= c_diff_left

            c[i] = self.combine(c_left, c_right)
            c_diff[i] = self.combine(c_diff_left, c_diff_right)

    def reverse_last_round(self, _set, key):
        _, _, c, c_diff = _set
        for i in range(self.num_plain):
            c_left, c_right = self.split(c[i])
            c_diff_left, c_diff_right = self.split(c_diff[i])

            c_left ^= self.f(c_right ^ key)
            c_diff_left ^= self.f(c_diff_right ^ key)

            c_left, c_right = c_right, c_left
            c_diff_left, c_diff_right = c_diff_right, c_diff_left

            c[i] = self.combine(c_left, c_right)
            c_diff[i] = self.combine(c_diff_left, c_diff_right)

    def crack_key(
        self, _set, o_diff, comparison, key_range=None, offset=0, list_key=None
    ):
        _, _, c, c_diff = _set

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
                    c_left, c_right = self.split(c[i])
                    c_diff_left, c_diff_right = self.split(c_diff[i])

                    f_out = c_left ^ self.f(c_right ^ key)
                    f_diff_out = c_diff_left ^ self.f(c_diff_right ^ key)

                    f_diff = f_diff_out ^ f_out
                    if f_diff & comparison != o_diff:
                        break
                    counter += 1

                if counter == self.num_plain and key not in res:
                    res.append(key)
                    yield key

    def crack_last_key(self, _set, comparison, key_range=None, offset=0, list_key=None):
        p, p_diff, c, c_diff = _set

        list_key = list_key or [0]
        key_range = key_range or 0x100000000
        offset *= 8

        res = []
        for k in list_key:
            for _k in range(key_range):
                key = k | (_k << offset)
                counter = 0
                for i in range(self.num_plain):
                    c_left, c_right = self.split(c[i])
                    p_left, _ = self.split(p[i])
                    c_diff_left, c_diff_right = self.split(c_diff[i])
                    p_diff_left, _ = self.split(p_diff[i])

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

        def _():
            # Crack Round 4
            set1 = self.get_set_choosen(diff1)
            self.reverse_final_operation(set1)

            key3 = self.crack_key(set1, out_diff, 0xFF, 0x10000)
            key3 = self.crack_key(set1, out_diff, 0xFFFFFFFF, 0x10000, 2, key3)
            # End Crack Round 4
            for k3 in key3:
                # Crack Round 3
                set2 = self.get_set_choosen(diff2)
                self.reverse_final_operation(set2)
                self.reverse_last_round(set2, k3)

                key2 = self.crack_key(set2, out_diff, 0xFF, 0x10000)
                key2 = self.crack_key(set2, out_diff, 0xFFFFFFFF, 0x10000, 2, key2)
                # End Crack Round 3

                for k2 in key2:
                    # Crack Round 2
                    set3 = self.get_set_choosen(diff3)
                    self.reverse_final_operation(set3)
                    self.reverse_last_round(set3, k3)
                    self.reverse_last_round(set3, k2)

                    key1 = self.crack_key(set3, out_diff, 0xFF, 0x10000)
                    key1 = self.crack_key(set3, out_diff, 0xFFFFFFFF, 0x10000, 2, key1)
                    # End Crack Round 2

                    for k1 in key1:
                        # Crack Round 1
                        set4 = self.get_set_choosen(diff4)
                        self.reverse_final_operation(set4)
                        self.reverse_last_round(set4, k3)
                        self.reverse_last_round(set4, k2)
                        self.reverse_last_round(set4, k1)

                        key0 = self.crack_last_key(set4, 0xFF, 0x10000)
                        key0 = self.crack_last_key(set4, 0xFFFFFFFF, 0x10000, 2, key0)
                        # End Crack Round 1

                        for k0 in key0:
                            f_key = [k0, k1, k2, k3]
                            flag = self.decrypt(self.c_flag, f_key)
                            if b"netcomp{" in flag and b"}" in flag:
                                print(flag)
                                return

        _()


Exploit().main()
