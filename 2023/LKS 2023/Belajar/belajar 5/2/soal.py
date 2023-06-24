

import random
from sympy import nextprime
from math import gcd
from Crypto.Util.number import *

flag = b"< REDACTED >"
flag = bytes_to_long(flag)

def gen_n():
  while True:
    n = 1
    phi = 1
    for i in range(4):
      candidate = nextprime(random.randrange(2**77,2**78))
      phi *= (candidate - 1)
      n *= candidate
    if gcd(phi,e) != 1:
      break
  return n

e = 3
n = gen_n()
c = pow(flag, e, n)

#n = 1850195628116871680423392008162891486298855759148914759564225087353621731522666807117150132479
#c = 1661751860305065872900880212931327639934266437307572764332159429755064632999907774437295003306
#e = 3

