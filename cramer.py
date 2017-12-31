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
			alpha1 = input('Choose your generators amongst {0} (comma separated) : '.format(prime_generators))
			if alpha1 not in prime_generators:
				raise ValueError


my_public = Public()
print my_public.create_public(7)
