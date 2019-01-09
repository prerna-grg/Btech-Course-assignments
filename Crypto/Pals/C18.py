import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import struct
from Crypto.Util.strxor import strxor

def CTR_encryption( plaintext ):	
	global iv_bytes
	global nonce
	keystream = b''
	while len(keystream) < len(plaintext):
		obj = AES.new(key, AES.MODE_ECB)
		keyblock = obj.encrypt(iv_bytes)
		nonce += 1
		iv_bytes = "".join(chr((nonce >> (i * 8)) & 0xFF) for i in range(16))
		a = iv_bytes[9:]
		iv_bytes = "".join( reversed(iv_bytes[:9])) + a
		keystream += keyblock

	if len(keystream) > len(plaintext):
		keystream = keystream[:len(plaintext)]

	ciphertext = strxor(plaintext, keystream)
	return ciphertext
    
def CTR_decryption( ciphertext ):
	global iv_bytes
	global nonce
	keystream = b''
	while len(keystream) < len(ciphertext):
		#print( ":".join("{:02x}".format(ord(c)) for c in iv_bytes))
		obj = AES.new(key, AES.MODE_ECB)
		keyblock = obj.encrypt(iv_bytes)
		nonce += 1
		iv_bytes = "".join(chr((nonce >> (i * 8)) & 0xFF) for i in range(16))
		a = iv_bytes[9:]
		iv_bytes = "".join( reversed(iv_bytes[:9])) + a
		keystream += keyblock

	if len(keystream) > len(ciphertext):
		keystream = keystream[:len(ciphertext)]

	plaintext = strxor(ciphertext, keystream)
	return plaintext
	
key = "YELLOW SUBMARINE"
nonce = 0
block_size = 16

string = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
nonce = 0
iv_bytes = "".join(chr((nonce >> (i * 8)) & 0xFF) for i in range(16))
iv_bytes = "".join( reversed(iv_bytes))

pt = CTR_decryption( string )
print(pt)

nonce = 0
iv_bytes = "".join(chr((nonce >> (i * 8)) & 0xFF) for i in range(16))
iv_bytes = "".join( reversed(iv_bytes))

ct = CTR_encryption( pt )
print(ct)

nonce = 0
iv_bytes = "".join(chr((nonce >> (i * 8)) & 0xFF) for i in range(16))
iv_bytes = "".join( reversed(iv_bytes))

pt = CTR_decryption( string )
print(pt)
