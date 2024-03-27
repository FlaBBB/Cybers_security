import sys

# sys.setrecursionlimit(100000)


class C:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return self.__str__()


class V:
    def __init__(self, *args):
        # print(f"args: {args}")
        # self.c = args[0] if args else None
        # if len(args) > 1:
        #     self.n = V(*args[1:])
        # else:
        #     self.n = None
        args = list(args)
        self.c = args.pop(0) if args else None
        self.n = None
        cur = None
        while args:
            if not self.n:
                self.n = V(args.pop(0))
                cur = self.n
                continue
            cur.n = V(args.pop(0))
            cur = cur.n

    def C(self, Y):
        # if self.n:
        #     return V(self.c, self.n.C(Y))
        # else:
        #     return V(self.c, Y)
        if not self.c:
            return V(Y)
        cur = self
        while cur.n:
            cur = cur.n
        cur.n = V(Y)
        return self

    def __str__(self):
        ans = f"{self.c}"
        cur = self.n
        while cur:
            ans += f",{cur.c}"
            cur = cur.n
        return ans

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        cur = self
        while cur:
            yield cur.c
            cur = cur.n


class secret(V):
    def __init__(self):
        super().__init__(
            C(438, 3190),
            C(102, 2664),
            C(58, 2712),
            C(229, 2954),
            C(219, 3452),
            C(69, 2647),
            C(311, 3002),
            C(303, 2647),
            C(284, 2988),
            C(3, 3081),
            C(830, 3274),
            C(-170, 2991),
            C(66, 2729),
            C(123, 2948),
            C(99, 2967),
            C(55, 2881),
            C(-50, 2920),
            C(169, 3152),
            C(204, 2551),
            C(328, 2709),
            C(-99, 2753),
            C(184, 2620),
            C(165, 2893),
            C(253, 2711),
            C(298, 2443),
            C(195, 3000),
            C(2, 2595),
            C(-164, 3003),
            C(555, 2977),
            C(-404, 2749),
            C(146, 3079),
            C(283, 2578),
        )


def G(i, a, b, c):
    for _ in range(i):
        a = (a * 171) % 30269
        b = (b * 172) % 30307
        c = (c * 170) % 30323
    return (a + b + c) % 32


class B:
    def __init__(self, T, i, j, k, *vals):
        # print(f"i: {i}, j: {j}, k: {k}, vals: {vals}")
        # if j > 0:
        #     self.M = B(
        #         T.C(
        #             V(
        #                 *vals,
        #                 C(
        #                     G(i * k + j - 1, 12643, 29806, 187),
        #                     G(i * k + j - 1, 3823, 25188, 24854),
        #                 ),
        #             )
        #         ),
        #         i,
        #         j - 1,
        #         k,
        #         *vals,
        #     )
        # elif i > 0:
        #     self.M = B(T.C(V(*vals)), i - 1, k, k, *vals)
        # else:
        #     self.M = T
        self.M = T
        for x in range(1, i + 1):
            for y in range(1, j + 1):
                self.M = self.M.C(
                    V(
                        *vals,
                        C(
                            G(x * k + y, 12643, 29806, 187),
                            G(x * k + y, 3823, 25188, 24854),
                        ),
                    )
                )


Key = B(V(), 31, 31, 31).M

max_p = 0


class P:
    @staticmethod
    def v(L, R, M):
        global max_p
        ans = 0
        i = 0
        while L & M:
            if i > max_p:
                # print(f"{i} = L: {L}, R: {R}, M: {M}")
                max_p = i
            ans += (L & M) * R
            L &= ~M
            M *= 2
            i += 1
        return ans
        # ans = 0
        # for _ in range(4):
        #     ans += (L & M) * R
        #     L &= ~M
        #     M *= 2
        # return ans


def v(L, R, M):
    ans = 0
    for i in range(64):
        ans += (L & (1 << i)) * R
    return ans


class Add:
    @staticmethod
    def r(L, R):
        return C(L.x + R.x, L.y + R.y)


class M:
    @staticmethod
    def r(L, R):
        return C(
            P.v(L.x, R.x, 1) - P.v(L.y, R.y, 1),
            P.v(L.x, R.y, 1) + P.v(L.y, R.x, 1),
        )


class smth:
    @staticmethod
    def r(L, R):
        # if L and R:
        #     print(f"L: {L}, R: {R}")
        #     return A.x(M.x(L.c, R.c), D.x(L.n, R.n).x)
        # else:
        #     return C(0, 0)
        ans = C(0, 0)
        while L and R:
            ans = Add.r(ans, M.r(L.c, R.c))
            L = L.n
            R = R.n
        # print(f"ans: {ans}")
        return ans


class Encrpyt:
    @staticmethod
    def r(Key, Msg):
        # if L:
        #     return Z.x(L.n, R).C(D.x(L.c, R).x)
        # else:
        #     return V()
        ans = V()
        while Key:
            ans = ans.C(smth.r(Key.c, Msg))
            Key = Key.n
        ans = V(list(ans)[::-1])
        # print(f"ans: {ans}")
        return ans


class E:
    @staticmethod
    def valid(L, R):
        if L and R:
            print(f"L: {L}, R: {R}")
            return (L.c.x == R.c.x) and (L.c.y == R.c.y) and E.valid(L.n, R.n)
        else:
            return True


# print(W.M)


class wctf:
    @staticmethod
    def valid(*Ts):
        return E.valid(Encrpyt.r(Key, V(*Ts)), secret())


_a = C(0, 1)
_b = C(1, 0)
_c = C(2, 0)
_d = C(1, 1)
_e = C(0, 2)
_f = C(3, 0)
_g = C(2, 1)
_h = C(1, 2)
_i = C(0, 3)
_j = C(4, 0)
_k = C(3, 1)
_l = C(2, 2)
_m = C(1, 3)
_n = C(0, 4)
_o = C(5, 0)
_p = C(4, 1)
_q = C(3, 2)
_r = C(2, 3)
_s = C(1, 4)
_t = C(0, 5)
_u = C(6, 0)
_v = C(5, 1)
_w = C(4, 2)
_x = C(3, 3)
_y = C(2, 4)
_z = C(1, 5)
_0 = C(0, 6)
_1 = C(7, 0)
_2 = C(6, 1)
_3 = C(5, 2)
_4 = C(4, 3)
_5 = C(3, 4)
_6 = C(2, 5)
_7 = C(1, 6)
_8 = C(0, 7)
_9 = C(8, 0)
__ = C(7, 1)

# print(W.M)
# # Example usage:
# print(
#     wctf.valid(_a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a, _a)
# )  # Output will be True or False
# w = list(W)
# print(w)
# print(len(w))
print(
    Encrpyt.r(
        Key,
        V(
            _a,
            _b,
            _c,
            _d,
            _e,
            _f,
            _g,
            _h,
            _i,
            _j,
            _k,
            _l,
            _m,
            _n,
            _o,
            _p,
            _q,
            _r,
            _s,
            _t,
            _u,
            _v,
            _w,
            _x,
            _y,
            _z,
            _0,
            _1,
            _2,
            _3,
            _4,
            _5,
            _6,
            _7,
            _8,
            _9,
            __,
        ),
    )
)
