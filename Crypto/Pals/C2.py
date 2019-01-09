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

str1 = "1c0111001f010100061a024b53535009181c"
str2 = "686974207468652062756c6c277320657965"

binary1 = ""
for i in range(len(str1)):
	a = hex_to_binary(str1[i])
	binary1 += a
binary2 = ""
for i in range(len(str2)):
	a = hex_to_binary(str2[i])
	binary2 += a
binary = xor(binary1 ,binary2)

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
print ( output )


