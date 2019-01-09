# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

obj = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
ciphertext =  base64.b64decode( "".join(list(open("7.txt", "r"))) )
if len(ciphertext)%16 != 0:
	print("Invalid Ciphertext")
	exit()
plaintext = obj.decrypt(ciphertext)
print(plaintext)
