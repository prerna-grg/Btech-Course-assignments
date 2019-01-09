import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict


block_size = 16

def repeated_blocks(buffer, block_length=16):
    reps = defaultdict(lambda: -1) # initialise every possible value with -1
    for i in range(0, len(buffer), block_length):
        block = bytes(buffer[i:i + block_length])
        reps[block] += 1 # will count the number of times this particular 16 bytes occurs
    return sum(reps.values())


def detect_ECB(ciphertext):
    ciphertext = ciphertext.rstrip()
    return repeated_blocks(bytearray(ciphertext))
	
def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ASCII')
	

def xor(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def encrypt_ECB(k , plaintext):
	plaintext = PKCS7_padding(plaintext , block_size)
	obj = AES.new( k , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext
	
def encrypt_CBC( IV , plaintext ):
	plaintext = PKCS7_padding(plaintext , block_size)
	obj = AES.new(key, AES.MODE_CBC, IV )
	ciphertext = obj.encrypt( plaintext )
	return ciphertext

def detect_oracle(ciphertext):
	return 0

def encryption_oracle(plaintext):
	before = randint(5, 10)
	after = randint(5,10)
	plaintext = plaintext.encode('ascii')
	for a in range(before):
		plaintext = os.urandom(16) + plaintext
	for a in range(after):
		plaintext = plaintext + os.urandom(16) 
	mode = randint(0,1)
	IV = os.urandom(16)
	if mode==0:
		# ECB encryption
		print ( "ECB encryption used")
		c = encrypt_ECB( key , plaintext )
	else:
		# CBC encryption
		print("CBC encryption used")
		c = encrypt_CBC( key , plaintext )
	same_bytes = detect_ECB(c)
	my_mode = 1
	if same_bytes>len(bytearray(plaintext))/64 :
		my_mode = 0
	if my_mode ==  0 :
		print ("ECB encryption detected")
	else:
		print ("CBC encryption detected")

with open ("C11.txt", "r") as myfile:
    plaintext = myfile.read().replace("\n","")

plaintext = plaintext.replace("\n" , "")
print(plaintext)
key = os.urandom(16)
encryption_oracle(plaintext)
