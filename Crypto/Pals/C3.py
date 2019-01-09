from operator import itemgetter


def get_score(text):
	english_freqs = [ 0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
	
	my_words = dict()
	for i in range(len(text)):
		if text[i] in my_words.keys():
			my_words[text[i]] += 1
		else:
			my_words[text[i]] = 1
	sorted(my_words.items(), key=lambda x:x[1] , reverse=True )
	list_count = [ [k,v] for k, v in my_words.items() ]
	list_count = sorted(list_count,key=itemgetter(1) , reverse = True )
	j=0
	chi_2 = 0
	for i,k in list_count:
		if i==' ' :
			pow( 0.13 - float(k/len(text))  , 2 ) / float(k/len(text)) 
		elif i>='a' and i<='z':
			chi_2 += pow( english_freqs[int(ord(i)-ord('a'))] - float(k/len(text))  , 2 ) / float(k/len(text)) 
		else:
			chi_2 += pow( float(k/len(text))  , 2 ) / float(k/len(text) )
	return chi_2


def hex_to_binary(num):
	if num>='0' and num<='9':
		num = int(num)
	else:
		num = int( ord(num)-ord('A') ) + 10
	output = ""
	for i in range(4):
		rem = num%2
		num = int(num/2)
		output = str(rem) + output
	return output

def getBase_16(num):
	if num>=0 and num<=9:
		return chr( ord('0') + num )
	elif num>=10 and num<=15:
		return chr( ord('a') + num-10 )
	else:
		return "#" 

def binary_to_hex(num):
	output = 0
	for i in range(4):
		if num[3-i]=='1':
			output += pow(2,i)
	return getBase_16(output)

def xor(num1,num2):
	if len(num1)!=len(num2):
		print ("Unequal Lengths")
		return "NULL"
	output = ""
	for i in range(len(num1)):
		if num1[i]==num2[i]:
			output += '0'
		else :
			output += '1'
	return output

def decimal_to_binary(num):
	out = ""
	for i in range(8):
		if num%2 == 0:
			out = "0" + out
		else:
			out = "1" + out
		num = int(num/2)
	return out

def binary_to_decimal(num):
	out = 0
	for i in range(8):
		if num[7-i]=='1':
			out = out + pow(2,i)
	return out


def bin_to_text(num):
	text = ""
	i = len(num)
	while len(num)>0:
		binary = num[:8]
		text = text + chr(binary_to_decimal(binary))
		num = num[8:]
	return text


def singleByteXorCipher( hex_num ):
	binary1 = ""
	for i in range(len(hex_num)):
		a = hex_to_binary(hex_num[i])
		binary1 += a
	
	if len(binary1)%8 !=0:
		while len(binary1)%8!=0:
			binary1 = '0' + binary1
	output = []
	for i in range(256):
		xor_me = decimal_to_binary(i)
		xor_s = xor_me
		while len(xor_s) < len(binary1):
			xor_s = xor_s + xor_me
		xor_ = xor(binary1 , xor_s )
		text_ = bin_to_text(xor_).lower()
		score_ = get_score(text_)
		output.append( [score_,xor_me,text_] )
	
	output = sorted(output, key=itemgetter(0))
	return output[:10]

str1 = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
keys = singleByteXorCipher(str1)
print("Top 10 possible keys and corresponding decryption")
print()
for i in keys:
	print(i)
	print()
