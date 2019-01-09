import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict

def PKCS7_unpadding(text):
	last = text[-1]
	for i in range(last):
		if text[-1] != last:
			return "lol"
		text = text[:-1]
	return text


def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ascii')


def create_obj( istr ):
	cobj = dict()
	objs = istr.split("&")
	for obj in objs:
		attr = obj.split("=")
		if len(attr)!=2:
			print("Error")
			return 0
		cobj[attr[0]] = attr[1]
	print (cobj)
	return cobj


def profile_for( obj ):
	global uid
	cobj = dict()
	obj = obj.replace('&' , '')
	obj = obj.replace('=' , '')
	cobj['email'] = obj
	cobj['uid'] = uid
	cobj['role'] = 'user'
	uid += 1
	pt = '&'.join(['%s=%s' % (k,cobj[k]) for k in ['email','uid','role']])
	ct = encrypt(pt)
	return ct
	
def encrypt(plaintext):
	plaintext = plaintext.encode('ascii')
	plaintext = PKCS7_padding(plaintext  , block_size)
	obj = AES.new( key , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext

def decrypt(ciphertext):
	obj = AES.new( key , AES.MODE_ECB)
	plaintext = obj.decrypt(ciphertext)
	plaintext = PKCS7_unpadding(plaintext)
	return plaintext

block_size = 16
key = os.urandom(16)
uid = 10
ct = profile_for("noobs@bar.com")
print(ct)
my_id = ct[:32]
ct = profile_for( (b"hahah@bar.admin" + (chr(11)*11).encode('ascii')).decode("utf-8") )
print(ct)
my_id = my_id + ct[16:32]
print(len(my_id))
pt = decrypt(my_id)
print(pt)
