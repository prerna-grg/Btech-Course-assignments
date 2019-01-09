import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict

block_size = 16
key = b'YELLOW SUBMARINE'

def PKCS7_unpadding(text):
	last = text[-1]
	for i in range(last):
		if text[-1] != last:
			return "lol"
		text = text[:-1]
	return text

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
	plaintext = '";"'.join(plaintext.split(';'))
	plaintext = '"="'.join(plaintext.split('='))
	plaintext = bytearray(plaintext , 'ascii')
	plaintext = b"comment1=cooking%20MCs;userdata=" + plaintext + b";comment2=%20like%20a%20pound%20of%20bacon"
	plaintext = PKCS7_padding(plaintext  , 16 )
	IV = os.urandom(16)
	obj = AES.new( key , AES.MODE_CBC , IV)
	ciphertext = obj.encrypt(plaintext)
	return IV+ciphertext

def decrypt(enc):
	IV = enc[:16]
	obj = AES.new( key, AES.MODE_CBC, IV )
	plaintext = obj.decrypt( enc )
	plaintext = PKCS7_unpadding(plaintext)
	return b';admin=true;' in plaintext


pt = ';admin=true'
ct = encryption_oracle(pt)
print(decrypt(ct))


