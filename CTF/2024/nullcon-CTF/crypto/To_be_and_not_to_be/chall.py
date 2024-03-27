#!/bin/python3
from Crypto.Util.number import isPrime
from secret import flag

class Random(object):
	def __init__(self):
		self.a = 17
		self.b = 324687
		self.state = 0
		self.mask = (1<<32) - 1

	def random_bytes(self, n):
		res = b''
		for _ in range(n):
			self.state = (self.a * self.state + self.b) & self.mask
			#print(self.state)
			res += int.to_bytes(self.state & 0xff,1,'big')
		return res

if __name__ == '__main__':
	p = int(input('p = '))
	assert 128 <= p.bit_length() <= 512
	R = Random()
	if isPrime(p, randfunc = R.random_bytes) and not isPrime(p, randfunc = R.random_bytes):
		print(flag)
