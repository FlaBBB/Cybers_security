#!/usr/bin/env python3

from sympy import nextprime
from Crypto.Util.number import *
from random import choice
from flag import flag


def get_prime(n):
	r = getRandomInteger(n)
	p = nextprime(r)
	q = nextprime(r + getRandomInteger(32))
	return p, q

def get_token(l):
	return ''.join(choice('0123456789abcdef') for i in range(l))


correct = 0
while correct < 100:
	token = get_token(32)
	p, q = get_prime(256)
	n = p * q
	e = 0x10001
	m = bytes_to_long(token.encode())
	c = pow(m,e,n)

	print(f'[*] {n = }')
	print(f'[*] {e = }')
	print(f'[*] {c = }')

	answer = input("[TOKEN]> ")
	if answer == token:
		correct += 1
		print()
	else:
		exit(0)

print(flag)