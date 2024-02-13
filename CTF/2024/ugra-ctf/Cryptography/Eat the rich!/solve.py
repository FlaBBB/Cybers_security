import gmpy2
import requests
from randcrack import RandCrack

BASE = "https://securityisamyth.q.2024.ugractf.ru"
# TOKEN = input("Enter token: ")
TOKEN = "tagibakd0rewso47"


p, g, y = [
    int(n, 16) for n in requests.post(f"{BASE}/{TOKEN}/get-parameters").text.split(", ")
]
inv_y = gmpy2.invert(y, p)

print("Computing, please wait...")
# rs = [random.randint(0, p - 2) for _ in range(32)]
# cs = [int(gmpy2.powmod(g, r, p)) for r in rs]
rc = RandCrack()

generated = g
generated |= y << 16384
for i in range(624):
    rc.submit(generated % 2**32)
    generated >>= 32
    assert generated != 0, "Not enough generated numbers"

while generated != 0:
    predicted = rc.predict_getrandbits(32)
    assert predicted == generated % 2**32, "Prediction failed"
    generated >>= 32

predicted_choices = rc.predict_getrandbits(32)
predicted_choices = [(predicted_choices >> i) & 1 for i in range(32)]

cs = []
answers = []
for pc in predicted_choices:
    ans = rc.predict_getrandbits(32)
    answers.append(ans)
    res = gmpy2.powmod(g, ans, p)
    if pc == 0:
        cs.append(int(res * inv_y % p))
    else:
        cs.append(int(res))

choices = eval(
    requests.post(
        f"{BASE}/{TOKEN}/announce-cs", data=b"".join(c.to_bytes(16384 // 8) for c in cs)
    ).text
)
assert predicted_choices == choices, "Prediction failed"

print("Verifying...")
result = requests.post(
    f"{BASE}/{TOKEN}/answer-choices",
    data=b"".join(answer.to_bytes(16384 // 8) for answer in answers),
).text
print(result)
