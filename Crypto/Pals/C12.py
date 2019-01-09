import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict

block_size = 16
key = os.urandom(block_size)

def repeated_blocks(buffer):
    reps = defaultdict(lambda: -1) # initialise every possible value with -1
    for i in range(0, len(buffer), block_size):
        block = bytes(buffer[i:i + block_size])
        reps[block] += 1 # will count the number of times this particular 16 bytes occurs
    return sum(reps.values())

def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ascii')

def encryption_oracle(plaintext):
	if type(plaintext) == type("a"):
		plaintext = plaintext.encode('utf-8')
	UNKNOWN_STRING = bytes(base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"))
	plaintext = plaintext + UNKNOWN_STRING
	plaintext = PKCS7_padding(plaintext  , block_size)
	obj = AES.new( key , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext
	
def detect_ECB(bs):
	plaintext = "A"*bs*2
	c = encryption_oracle(plaintext)
	if( repeated_blocks(bytearray(c)) > 0 ):
		return True
	return False

def getBlockSize():
	plaintext = "A"
	while True:
		c = encryption_oracle(plaintext)
		if( repeated_blocks(bytearray(c)) > 0 ):
			return round(len(plaintext)/2)
		plaintext += "A"

def my_decryption():
	
	bs = getBlockSize()
	print("Block size = " + str(bs))
	print("ECB mode? " + str(detect_ECB(bs)) )
		
	i = 1
	my_string = ""
	#limit = 
	while i<bs+1:
		my_dict = dict()
		my_str = "A"*(bs-i) + my_string
		for j in range(256):
			my_dict[encryption_oracle(my_str+chr(j))[:bs]] = chr(j)
		my_str = "A"*( bs - i)
		c = encryption_oracle(my_str)
		c = c[:bs]
		if c in my_dict:
			my_string = my_string + my_dict[c]
		else:
			return my_string
		i += 1
		if i==bs+1:
			bs = bs + bs
			

print("\nThe unknown string is : " )
print(my_decryption())
