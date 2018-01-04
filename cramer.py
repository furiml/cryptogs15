#!/usr/bin/env python

import random

Errors = (ValueError, NameError)
# error handling easier using a tuple later on

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
			for i in xrange(s - 1):
				if x == n - 1:
					return True
				x = pow(x, 2, n)
			return x == n - 1
		s = 0
		d = n - 1
		while d % 2 == 0:
			d >>= 1
			s += 1
		for i in xrange(k):
			a = random.randrange(2, n - 1)
			if not check(a, s, d, n):
				return False
		return True

	def create_public(self):
		while True :
			try :
				input_prime = int(input('Choose a prime : '))
				if not self.is_prime(input_prime):
					raise ValueError
				print 'Good job ! Listing {}\'s generators...'.format(input_prime)	
			except ValueError :
				print 'Your choice isn\'t a prime'
			else :
				break

		# generators listing
		prime_generators = []
		for i in range (2,input_prime):
			for j in range (1,input_prime):
				if (i**j) % input_prime == (1 % input_prime):
					if j == input_prime - 1:
						prime_generators.append(i)
					else :
						break

		# variables definitions
		while True :
			prime_generators_dummy = prime_generators
			try :
				alpha1 = int(input('Choose your first generator amongst {} : '.format(prime_generators_dummy)))
				if alpha1 in prime_generators_dummy :
					prime_generators_dummy.remove(alpha1)
				else :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t in the generator list. Try again.'
				continue
			else : 
				break
		if len(prime_generators_dummy) == 1 : # after we remove the chosen generator, if there's only one remaining, choose it
			print 'Only one generator left. Automatically choosing {} as second generator.'.format(prime_generators_dummy[0])
			alpha2 = prime_generators_dummy[0]
		else :
			while True :
					try :
						alpha2 = int(input('Choose your second generator amongst {} : '.format(prime_generators_dummy)))
						if alpha2 not in prime_generators_dummy :
							raise ValueError
					except Errors :
						print 'Your choice wasn\'t in the generator list. Try again.'
						continue
					else :
						break
		
		def try_input(self, msg, prime):
			while True :
				try :
					user_input = input(msg)
					if user_input > prime :
						raise ValueError
				except Errors :
					print 'Your choice wasn\'t smaller than {}. Try again.'.format(prime)
					continue
				else :
					print type(user_input)
					break
			return user_input

		x1 = try_input(self,'Choose a first integer (x1) smaller than {} : '.format(input_prime),input_prime)
		x2 = try_input(self,'Choose a second integer (x2) smaller than {} : '.format(input_prime),input_prime)
		y1 = try_input(self,'Choose a third integer (y1) smaller than {} : '.format(input_prime),input_prime)
		y2 = try_input(self,'Choose a fourh integer (y2) smaller than {} : '.format(input_prime),input_prime)
		w_input = try_input(self,'Choose a last integer (w) smaller than {} : '.format(input_prime),input_prime)

		# calculate x, y, and w
		x = (alpha1**x1)*(alpha2**x2)
		y = (alpha1**y1)*(alpha2**y2)
		w = alpha1**w_input
		return (input_prime, alpha1, alpha2, x, y, w)


my_public = Public()
print my_public.create_public()
