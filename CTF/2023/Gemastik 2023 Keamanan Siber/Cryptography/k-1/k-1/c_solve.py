import random
import sys

sys.set_int_max_str_digits(1000000)

class chall:
    bits = 1024
    k = random.randint(20, 35)
    __password = random.getrandbits(bits) % 1000000

    def get_shares(self):
        coeffs = [self.__password] + [random.getrandbits(self.bits) for _ in range(self.k - 1)]
        # print(coeffs)
        x_list = set()
        while len(x_list) < self.k - 1:
            x_list.add(random.getrandbits(self.bits))
        
        shares = []
        for x in x_list:
            y = sum(map(lambda i : coeffs[i] * pow(x, i), range(len(coeffs))))
            shares.append((x, y))
        
        return shares

    def check_password(self, res):
        if self.__password == res:
            print('gg')


def solve(k, shares) -> int:
    pass

challenge = chall()

shares = challenge.get_shares()
print(shares)


res = solve(challenge.k, shares)
challenge.check_password(res)