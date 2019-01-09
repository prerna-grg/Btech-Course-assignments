import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict

block_size = 16
prefix = os.urandom(200)
key = "YELLOW SUBMARINE"


def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ascii')


def repeated_blocks(buffer):
	for i in range(0, len(buffer), block_size):
		if i+2*block_size > len(buffer) :
			return None
		block_i = bytes(buffer[i:i + block_size])
		block_i1 = bytes(buffer[i+block_size:i + 2*block_size])
		if block_i == block_i1:
			print(i)
			return i
	return None
    

def encryption_oracle(plaintext):
	block_size = 16
	if type(plaintext) == type("a"):
		plaintext = plaintext.encode('utf-8')
	UNKNOWN_STRING = bytes(base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))
	plaintext = prefix + plaintext + UNKNOWN_STRING
	plaintext = PKCS7_padding(plaintext  , block_size)
	obj = AES.new( key , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext
	

def detect_ECB(block_size):
	plaintext = "A"*block_size*2
	c = encryption_oracle(plaintext)
	if( repeated_blocks(bytearray(c)) > 0 ):
		return True
	return False

def my_decryption():
	global block_size
	start_size = 32
	i=0
	while True:
		my_string = b'A'*(start_size+i)
		ct = encryption_oracle(my_string)
		#print("hi_1")
		index = repeated_blocks(ct)
		if index != None:			
			print("Size of prefix:", index - i )
			break
		i+=1
	extra = i
	i=1
	my_string = ""
	while i<block_size+1:
		my_dict = dict()
		my_str = "A"*(extra+block_size-i) + my_string
		for j in range(256):
			my_dict[encryption_oracle(my_str+chr(j))[:index+block_size]] = chr(j)
		my_str = "A"*( extra+block_size-i)
		c = encryption_oracle(my_str)
		c = c[:index+block_size]
		if c in my_dict:
			my_string = my_string + my_dict[c]
		else:
			return my_string
		i += 1
		if i==block_size+1:
			block_size = block_size + block_size
	

print(my_decryption())
