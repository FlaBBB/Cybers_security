from Cryptodome.Util.number import *
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

from hashlib import sha256

kbits = 200

x = 2979367707659603116523387035539295735026485376436807443084845278516127174929783019392967820185018635850079566349868983092853995552241574450881758637291247
c2 = 1170023119885859101024387880045520537874087001683337675848090433661429128088166458798239305574743731841113872001902781327295181878803694961875127813114856
p = 13380037624452997384558524852608866433273618414151667350982539548293385222637966469911875057641453772347655559134636498494634474259294446532131041568362471
iv = bytes.fromhex('8c1d85feea24c3145ace02cb86c79e07')
ct = bytes.fromhex('732c41662a780f0d7784d2d91845556cb258a5f413c218e9f5618d9d5eada1d7356c755eb121e25ee3d9299b2039a45b')

y = (p^^x) & ((2**(512-kbits)-1) << kbits)
C = (c2 - x*y - y) % p
N = p

def check(M):
  for m in M:
    if m[3] == 0 and m[0] > 0 and m[0] < 2**200:
      return True, m[0], m[1]
  return False, 0, 0

for k in range(1,200):
    w = 2**k #weight
    m = [[1,0,0,w*x], [0,1,0,w], [0,0,w,w*C], [0,0,0,w*N]]
    n = len(m)
    M = Matrix(ZZ, n)
    for i in range(n):
      for j in range(n):
        M[i, j] = m[i][j]
    L = M.LLL() 
    if check(L)[0]:
      print(k)
      X, Y = check(L)[1], check(L)[2]
      break

a = X + y
b = Y + y

key = sha256(long_to_bytes(a) + long_to_bytes(b)).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct),16)
print(flag)