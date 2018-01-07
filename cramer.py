#!/usr/bin/env python3

import secrets
import random
import binascii
import hashlib
import math

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

def random_smaller(self, mini, maxi):
	s_r = secrets.SystemRandom()
	return s_r.randrange(mini,maxi)

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
		x1 = random_smaller(self,1,input_prime)
		x2 = random_smaller(self,1,input_prime)
		y1 = random_smaller(self,1,input_prime)
		y2 = random_smaller(self,1,input_prime)
		w_input = random_smaller(self,1,input_prime)

		priv = (x1,x2,y1,y2,w_input)
		priv_str = str(priv)
		priv_file = open('key.priv','w')
		priv_file.write(priv_str + '\n')
		priv_file.close()
		# calculate x, y, and w
		x = int(pow(alpha1,x1) * pow(alpha2,x2) % input_prime)
		y = int(pow(alpha1,y1) * pow(alpha2,y2) % input_prime)
		w = int(pow(alpha1,w_input,input_prime))
		# as we return all the elements in a tuple, mind the index !
		pub = (input_prime, alpha1, alpha2, x, y, w)
		pub_str = str(pub)
		pub_file = open('key.pub','w')
		pub_file.write(pub_str + '\n')
		pub_file.close()
		return pub

class Encryption:
	def __init__(self):
		global Errors
		return

	def pad(self,m,s):
		"""
		Add zeros at the end of the message to complete the block
		m: message
		s: size of the blocks
		"""
		binary = bin(int(binascii.hexlify(m),16))[2:]
		binary = binary.zfill(len(binary) + 8-(len(binary) % 64))
		binary = binary + '0'*(s - (len(binary) % s))
		binary = [binary[i:i+s] for i in range(0, len(binary), s)]
		return binary


	def create_coded(self, pub_key_file, msg):
		try :
			with open(pub_key_file) as f :
				pub = eval(f.read())
		except :
			print('File not found.')
		m = self.pad(msg.encode(),8)
		# print('message haché + paddé : {}'.format(m))
		b = random_smaller(self,1,pub[0])
		# print('b is {}'.format(b))
		coded = []
		for i in m :
			b1 = pow(pub[1],b,pub[0])
			b2 = pow(pub[2],b,pub[0])
			c = pow(pow(pub[5],b,pub[0]) * int(i,2),1,pub[0])
			temp_list = [str(b1),str(b2),str(c)]
			mysha = ''.join(temp_list)
			sha = hashlib.sha512()
			sha.update(mysha.encode('utf-8'))
			beta = sha.hexdigest()
			v = pow(pow(pub[3],b,pub[0]) * pow(pub[4],b*int(beta,16),pub[0]),1,pub[0])
			coded.append((b1,b2,c,v))
		coded_file = open('coded.crypt','w')
		for i in coded :
			for j in i :
				coded_file.write(bin(j)[2:])
		coded_file.write('\n')
		coded_file.close()
		return coded

class Decryption:
	def __init__(self):
		global Errors
		return

	def verify(self,coded,priv_key_file,pub_key_file):
		try:
			with open(priv_key_file) as f :
				priv = eval(f.read())
			with open(pub_key_file) as f :
				pub = eval(f.read())
		except :
			print('File not found.')
		for i in coded :
			temp_hash = []
			for j in i :
				temp_hash.append(str(j))
			sha = hashlib.md5()
			sha.update(''.join(temp_hash).encode('utf-8'))
			betaprim = sha.hexdigest()
			vprim = (pow(i[0],priv[0],pub[0]) * pow(i[1],priv[1],pub[0]) * pow(pow(i[0],priv[2],pub[0]) * pow(i[1],priv[3],pub[0]),int(betaprim,16),pub[0])) % pub[0]
			if vprim != i[3] :
				raise ValueError('La vérification a échoué au bloc {}'.format(i))
		return


my_public_key = Public().create_public()
coded = Encryption().create_coded('key.pub','Hi, i am a message which is several bytes long')
#  print('codé : {}'.format(coded))
decode = Decryption().verify(coded,'key.priv','key.pub')