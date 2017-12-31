#!/usr/bin/env python

import random

class Public:
	def __init__(self):
		return

	def create_public(self,input_prime):
		prime_generators = []
		for i in range (2,input_prime):
			for j in range (1,input_prime):
				if (i**j) % input_prime == (1 % input_prime):
					if j == input_prime - 1:
						prime_generators.append(i)
					else :
						break
		while True:
			prime_generators_dummy = prime_generators
			alpha1 = input('Choose your first generator amongst {} : '.format(prime_generators_dummy))
			if alpha1 in prime_generators_dummy :
				prime_generators_dummy.pop(index(alpha1))
			else :
				raise ValueError
			alpha2 = input('Choose your second generator amongst {} : ').format(prime_generators_dummy)
			if alpha2 not in prime_generators_dummy :
				raise ValueError

my_public = Public()
print my_public.create_public(7)
