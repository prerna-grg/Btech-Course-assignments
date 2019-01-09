import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

key = "YELLOW SUBMARINE"
block_size = 16


def xor(s1,s2):
	return ''.join(chr(a ^ b) for a,b in zip(s1,s2))

def decrypt(text):
	obj = AES.new( key , AES.MODE_ECB)
	plaintext = obj.decrypt(text)
	return plaintext
	
plaintext = ""

with open ("C10.txt", "r") as myfile:
    ciphertext = myfile.read().replace("\n","")

ciphertext = base64.b64decode( ciphertext.rstrip()) # convert to ascii
print(len(ciphertext))
print( ciphertext[:5] )

if len(ciphertext)%16!=0:
	print("Error")
IV = ("0"*16).encode("ASCII")

while len(ciphertext)!=0:
	next_block = ciphertext[:16]
	mi_c1 = decrypt(next_block)
	plaintext += xor(mi_c1,IV)
	IV = next_block
	ciphertext = ciphertext[16:]
plaintext += "\n"

print(plaintext)

