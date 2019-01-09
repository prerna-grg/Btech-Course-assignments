import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

key = os.urandom(16)
block_size = 16

strings = [ "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=" , 
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=" , 
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==" ,
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93" ]

def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	print(type(chr(amount_to_pad) * amount_to_pad))
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ASCII')

def encryption_oracle(plaintext):
	plaintext = PKCS7_padding(plaintext , block_size)
	obj = AES.new( key , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext

def decryption_oracle(ciphertext):
	obj = AES.new( key , AES.MODE_ECB)
	plaintext = obj.decrypt(ciphertext)
	return plaintext
	
def check_padding(plaintext):
	last = plaintext[-1]
	for i in range(last):
		if plaintext[-i-1] != last:
			return False
	return True
	

index = randint(0, 9)
plaintext = base64.b64decode(strings[index])
print(type(plaintext))
ct = encryption_oracle(plaintext)
#print(ct)
pt = decryption_oracle(ct)
#print(pt)
print(check_padding(pt))

	
