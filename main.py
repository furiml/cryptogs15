#!/usr/bin/env python
#[looks like there is some python here]

# TODO : document generate_key() and generate_tweaks()

import os,binascii
# os is for random bytes generation
# binascii is used for conversion between ascii, hex & binary representation
possible_key_size = [256,512,1024]
# possible sizes for the original key
c_const = 0x1bd11bdaa9fc1a22
# see subject

DEBUG=0

def debug(str):
	if DEBUG:
		print str

class Key:
	def __init__(self):
		global possible_key_size
		global c_const
		return

	def generate_key(self, key_size):
		key = binascii.b2a_hex(os.urandom(key_size/8))
		key_chunks = []
		# we use a list to generate the chunks
		for i in xrange(0, key_size/4,16):
			key_chunks.append(''.join(key[i:i+16]))
			# divides the original key in 4, 64 bits long chunks
		last_chunk = c_const
		for i in key_chunks:
			last_chunk = last_chunk ^ int(i,16)
			# xors the 4 original chunks and c_const to get the last chunk
		key_chunks.append(hex(last_chunk)[2:-1])
		# appends it in hex representation : 0x167...L
		# [2:-1] is used to strip unused characters '0x' and 'L' in the hex representation 
		return {'Key': key_chunks, 'Key_Size': key_size}
		# returns the key and its size in a dic
		# we leave the key in form of a list of 5 chunks for later

	def generate_tweaks(self, tweaks_dic):
		# tweaks are random 8 bytes words
		# we'll use this later, in the tour keys generation
		tweaks_dic.update({'Tweak0': binascii.b2a_hex(os.urandom(8))})
		tweaks_dic.update({'Tweak1': binascii.b2a_hex(os.urandom(8))})
		tweaks_dic.update({'Tweak2': hex(int(tweaks_dic['Tweak0'],16) ^ int(tweaks_dic['Tweak1'],16))[2:-1]})
		# xors tweak0 and tweak1 to get tweak2
		return tweaks_dic

		# --------------------------------------------------- #
		# below this, we plan to do a step by step generation #
		# not used atm.										  #
		# --------------------------------------------------- #

	def step_generate_key(self, key_size):
		"""
		Generates a hex string 256, 512 or 1024 bits long
		"""
		if key_size not in possible_key_size :
			raise ValueError('saisie invalide')
		key_holder = binascii.b2a_hex(os.urandom(key_size/8))
		return key_holder

	def step_chunkify_key_step(self, key_word):
		"""
		Split the argument string into chunks of 64 bits
		(4, 8 or 16 chunks)
		"""
		key_list = list(key_word)
		key_chunks = []
		for i in xrange(0, len(key_word),16):
			key_chunks.append(''.join(key_list[i:i+16]))
		return key_chunks

	def step_add_last_chunk(self, key_chunks):
		"""
		Adds the last chunk to the key, which is a xor of c_const
		and the other chunks
		"""
		last_chunk = c_const
		for i in key_chunks:
			last_chunk = last_chunk ^ int(i,16)
		key_chunks.append(hex(last_chunk)[2:-1])
		return key_chunks

		# ---------------------------------- #
		# step by step generation stops here #
		# ---------------------------------- #

	def generate_tour_keys(self):
		"""
		Generates 20 tour keys based on the instructions provided by our beloved guru, R.C.
		"""
		tour_keys={}
		# tour keys will be in form of lists stored in a dic named tour_keys
		for i in range(20):
			tour_keys['tour_key{0}'.format(i)] = []
			# creates 20 lists names tour_key0, tour_key1, ... in the tour_keys dic
		tweaks={}
		# we generate tweaks now
		tweaks = self.generate_tweaks(tweaks)

		# ------------------------------------- #
		# first tour generation starts here 	#
		# it has some special aspects which is  #
		# why we generate it before other tours #
		# ------------------------------------- #
			# chunk 1 (from 0 to N-4)
		for i in range((my_key['Key_Size'] / 64) - 3):
			tour_keys['tour_key0'].append(my_key['Key'][i])
			# chunk 2 (N-3)
		tour_keys['tour_key0'].append(hex((int(my_key['Key'][(my_key['Key_Size'] / 64) - 3],16) + int(tweaks['Tweak0'],16)) % (2**64))[2:-1])
			# chunk 3	 (N-2)
		tour_keys['tour_key0'].append(hex((int(my_key['Key'][(my_key['Key_Size'] / 64) - 2],16) + int(tweaks['Tweak1'],16)) % (2**64))[2:-1])
			# chunk 4 (N-1)
		tour_keys['tour_key0'].append(hex((int(my_key['Key'][(my_key['Key_Size'] / 64) - 1],16) + 0) % (2**64))[2:-1])

		# -------------------------------- #
		# first tour generation stops here #
		#				   #
		# and loop generation starts here  #
		# -------------------------------- #
		for i in range(1,20):
			for j in range ((my_key['Key_Size'] / 64) - 3):
				# chunk 1
				tour_keys['tour_key{0}'.format(i)].append(my_key['Key'][(i + j) % ((my_key['Key_Size'] / 64) + 1)])
				# chunk 2 mind the wrap
			tour_keys['tour_key{0}'.format(i)].append(hex((int(my_key['Key'][(i + (my_key['Key_Size'] / 64) - 3) 
				% ((my_key['Key_Size'] / 64) + 1)],16) + int(tweaks['Tweak{}'.format(i % 3)],16)) % (2**64))[2:-1])
				# chunk 3 mind the wrap
			tour_keys['tour_key{0}'.format(i)].append(hex((int(my_key['Key'][(i + (my_key['Key_Size'] / 64) - 2) 
				% ((my_key['Key_Size'] / 64) + 1)],16) + int(tweaks['Tweak{}'.format((i + 1)% 3)],16)) % (2**64))[2:-1])
				# chunk 4 mind the wrap
			tour_keys['tour_key{0}'.format(i)].append(hex((int(my_key['Key'][(i + (my_key['Key_Size'] / 64) - 1) 
				% ((my_key['Key_Size'] / 64) + 1)],16) + i))[2:-1])
		
		# pad and concatenates the chunks
		for i in range(0,20):
			debug(tour_keys['tour_key{0}'.format(i)])
			temp = ""
			for e in tour_keys['tour_key{0}'.format(i)]:
				new = '0'*(16-len(e))+e
				debug(new)
				temp += new
			debug(temp)
			tour_keys['tour_key{0}'.format(i)] = temp
			debug("")
		
		# and returns the dictionnary
		return tour_keys		

class Encryption:
	def __init__(self, m, s, keyset):
		self.block_size = s
		message = m
		self.keyset = keyset
		# generer les cles ici
		self.tf_ecb_main(self.pad(message,self.block_size),keyset)
		return

	def rot(self,m,k,n):
		"""
		Perform a binary left rotation of the message (ie. 0100 -> 1000 if k = 1)
		m: message to rotate
		k: number of bits to rotate
		n: size of the message
		"""
		return ((m<<k)|(m>>(n-k)))&((1<<n)-1)

	def mix(self,m1,m2):
		"""
		Mix a pair of words (64 bits)
		"""
		m1_new = int(m1,2) + int(m2,2) % (2**64)
		m2_new = m1_new ^ self.rot(int(m2,2),1,64)
		return bin(m1_new),bin(m2_new)

	def permutation(self,b):
		return b

	def pad(self,m,s):
		"""
		Add zeros at the end of the message to complete the block
		m: message
		s: size of the blocks
		"""
		binary = bin(int(binascii.hexlify(m),16))[2:]
		binary = binary.zfill(len(binary) + 8-(len(binary) % 8))
		binary = binary + '0'*(s - (len(binary) % s))

		debug("Formatted message :")
		debug(binary)
		debug("")
		return binary

	def pad_left(self,b,s):
		"""
		Add zeros at the begining of a number
		b: binary number
		s: size of the block
		"""
		return '0'*(s - len(b)) + b

	def tf_ecb_main(self, m, keys):
		encrypted_message = []
		chunked_message = [m[i:i+self.block_size] for i in range(0, len(m), self.block_size)]

		# ECB = idependant treatment of each block
		for id_b, b in enumerate(chunked_message):
			debug("Chunked message #",id_b,":")
			debug("")
			debug("===================== TOUR 0 =====================")
			# Init with tour_key0
			debug("HEX;",hex(int(b,2)))
			debug("KEY:",hex(int(keys['tour_key0'],16)))
			debug("RES:",hex((int(b,2) ^ int(keys['tour_key0'],16))))
			# For each block, we create a crypted block. Blocks are not related
			encrypted_message.append(hex((int(b,2) ^ int(keys['tour_key0'],16))))
			debug("")
			
			for k in range(1,20): # loop through tour_keys
				debug("===================== TOUR",k,"=====================")
				# Extract words (64 bits)
				b_words = [b[i:i+64] for i in range(0, len(b), 64)]
				debug(b_words)

				# mix
				for w in range(0,len(b_words)/2): # for every pair of words
					b_words_new = self.mix(b_words[w*2],b_words[w*2+1])
					b_words[w*2]   = self.pad_left(b_words_new[0][2:],64)
					b_words[w*2+1] = self.pad_left(b_words_new[1][2:],64)
					debug("(mix)")
				
				debug(b_words)

				# permutation
				self.permutation(b_words)
				debug("HEX;",hex(int(b,2)))
				debug("KEY:",hex(int(keys['tour_key{0}'.format(k)],16)))
				debug("RES:",hex((int(b,2) ^ int(keys['tour_key{0}'.format(k)],16))))
				debug("")
		return 1
		

# ---------- # 
# here we go #
# ---------- #
key = Key()
while True :
	try :
		B_SIZE = int(input('Choose a key size (256, 512 or 1024 bits) : '))
		if B_SIZE not in possible_key_size :
			raise ValueError
	except ValueError :
		print 'Invalid size. Try again.'
		continue
	else :
		break
my_key = key.generate_key(B_SIZE)
print 'My key is :',
print my_key['Key']

print ""

print 'Tour keys:'
my_tour_keys = key.generate_tour_keys()
print my_tour_keys

print ""

enc = Encryption("Coucou comment ca va ? Moi ca va pas mal, meme si je suis oblige de bosser ca pendant les vacances, car je veux mon master",B_SIZE,my_tour_keys)
