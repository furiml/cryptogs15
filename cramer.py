#!/usr/bin/env python

import random

Errors = (ValueError, NameError)
# error handling easier using a tuple later on

class Public:
	def __init__(self):
		global Errors
		return

	def create_public(self):
		while True :
			try :
				input_prime = int(input('Choose a prime : '))
			except ValueError :						# TODO : tester si input_prime est premier
				print 'Your choice isn\'t a prime'	# TODO 
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
				alpha1 = input('Choose your first generator amongst {} : '.format(prime_generators_dummy))
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
		# now we choose the integers x1, x2, y1, y2, w
		while True :
			try :
				x1 = input('Choose an integer (x1) smaller than {} : '.format(input_prime))
				if x1 > input_prime :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t smaller than {}. Try again'.format(input_prime)
				continue
			else :
				break
		while True :
			try :
				x2 = input('Choose a second integer (x2) smaller than {} : '.format(input_prime))
				if x2 > input_prime :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t smaller than {}. Try again'.format(input_prime)
				continue
			else : 
				break
		while True :
			try :
				y1 = input('Choose a third integer (y1) smaller than {} : '.format(input_prime))
				if y1 > input_prime :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t smaller than {}. Try again'.format(input_prime)
				continue
			else : 
				break
		while True :
			try :
				y2 = input('Choose a fourth integer (y2) smaller than {} : '.format(input_prime))
				if y2 > input_prime :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t smaller than {}. Try again'.format(input_prime)
				continue
			else : 
				break
		while True :
			try :
				w_input = input('Choose a last integer (w) smaller than {} : '.format(input_prime))
				if w_input > input_prime :
					raise ValueError
			except Errors :
				print 'Your choice wasn\'t smaller than {}. Try again'.format(input_prime)
				continue
			else :
				break
		# calculate x, y, and w
		x = (alpha1**x1)*(alpha2**x2)
		y = (alpha1**y1)*(alpha2**y2)
		w = alpha1**w_input
		return (input_prime, alpha1, alpha2, x, y, w)


my_public = Public()
print my_public.create_public()
