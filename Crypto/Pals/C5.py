def decimal_to_binary(num):
	out = ""
	for i in range(8):
		if num%2 == 0:
			out = "0" + out
		else:
			out = "1" + out
		num = int(num/2)
	return out

def text_to_bin(text):
	out = ""
	for i in range(len(text)):
		num = ord(text[i])
		out = out + decimal_to_binary(num)
	return out

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

def ImplementrepeatingkeyXOR(key , text):
	bin1 = text_to_bin(text)
	key = text_to_bin(key)
	key_ = key
	while len(key_)<len(bin1):
		key_ = key_ + key
	key_ = key_[:len(bin1)]
	binary = xor(key_,bin1)
	output = ""
	i=len(binary)
	while i>=0:
		if i-4 < 0 :
			while len(binary)!=4:
				binary = '0' + binary
			if binary != "0000":
				output = binary_to_hex(binary) + output
			i=-1
		else:
			output = binary_to_hex(binary[i-4:i]) + output
			binary = binary[:i-4]
			i = i-4
	return output

str1 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"
print(ImplementrepeatingkeyXOR(key,str1))
