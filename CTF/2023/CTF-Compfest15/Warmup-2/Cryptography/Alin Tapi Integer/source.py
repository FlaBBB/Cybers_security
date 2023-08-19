import random
import numpy as np

m = np.array([123456789, 987654321])
r = np.array([[random.getrandbits(100), random.getrandbits(100)], [random.getrandbits(100), random.getrandbits(100)]])
e = np.array([random.getrandbits(100), random.getrandbits(100)])

c = np.dot(e, r) + m

print("r = {}".format(r))
print("c = {}".format(c))