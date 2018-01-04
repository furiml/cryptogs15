#!/usr/bin/env python3

import secrets
import random
import sys

# error handling easier using a tuple later on
Errors = (ValueError, NameError, IndexError)

# tries user input
def try_input(self, msg, integer):
			while True :
				try :
					user_input = int(input(msg))
					if user_input > integer :
						raise ValueError
				except Errors :
					print('Your choice wasn\'t smaller than {}. Try again.'.format(integer))
					continue
				else :
					break
			return user_input

class Public:
	def __init__(self):
		global Errors
		return

	def is_prime(self, n, k=10):		# Found this Miller-Rabin. Must learn how it works.
		if n == 2:
			return True
		if not n & 1:
			return False

		def check(a, s, d, n):
			x = pow(a, d, n)
			if x == 1:
				return True
			for i in range(s - 1):
				if x == n - 1:
					return True
				x = pow(x, 2, n)
			return x == n - 1
		s = 0
		d = n - 1
		while d % 2 == 0:
			d >>= 1
			s += 1
		for i in range(k):
			a = random.randrange(2, n - 1)
			if not check(a, s, d, n):
				return False
		return True

	def create_public(self):
		# function for testing if an input is smaller than selected prime
		
		# user query
		while True :
			try :
				input_prime = int(input('Choose a strong prime : '))
				if not self.is_prime(input_prime):
					raise ValueError('Your number isn\'t a prime.')
				q = int((input_prime - 1) / 2)
				if not self.is_prime(q):
					raise ValueError('Your number isn\'t a strong prime.')
			except Errors as error:
				print('Caught an error : {}'.format(repr(error)))
			else :
				break

		# generators listing
		prime_generators = []
		s_r = secrets.SystemRandom()
		while len(prime_generators) != 2 :
			i = s_r.randrange(2,input_prime)
			order1 = pow(i,2,input_prime)
			order2 = pow(i,q,input_prime)
			if order1 != 1 and order2 != 1:
				prime_generators.append(i)
			if len(prime_generators) == 2 and prime_generators[0] == prime_generators[1] :
				prime_generators.pop(0)

		alpha1 = prime_generators[0]
		alpha2 = prime_generators[1]
		x1 = s_r.randrange(1,input_prime)
		x2 = s_r.randrange(1,input_prime)
		y1 = s_r.randrange(1,input_prime)
		y2 = s_r.randrange(1,input_prime)
		w_input = s_r.randrange(1,input_prime)

		# calculate x, y, and w
		x = int(pow(alpha1,x1) * pow(alpha2,x2) % input_prime)
		y = int(pow(alpha1,y1) * pow(alpha2,y2) % input_prime)
		w = int(pow(alpha1,w_input,input_prime))
		# as we return all the elements in a tuple, mind the index !
		return (input_prime, alpha1, alpha2, x, y, w)

class Encryption:
	def __init__(self):
		global Errors
		return
	def create_coded(self, public_key):
		b = try_input(self,'Choose an integer smaller than {} : '.format(public_key[0]), public_key[0])
		b1 = public_key[1]**b
		b2 = public_key[2]**b
		c = (public_key[5]**b) * m


# my_public = Public()
my_public_key = Public().create_public()
print(my_public_key)