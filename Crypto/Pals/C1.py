def getBase_64(num):
	if num>=0 and num<=25:
		return chr( ord('A') + num )
	elif num>=26 and num<=51:
		return chr( ord('a') + num-26 )
	elif num>=52 and num<=63:
		return chr( ord('0') + num-52 )
	else:
		return "#" 


def binary_to_base64(num):
	output = 0
	for i in range(6):
		if num[5-i]=='1':
			output += pow(2,i)
	return getBase_64(output)

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


def hex_to_base64(string):
	binary = ""
	for i in range(len(string)):
		a = hex_to_binary(string[i])
		binary += a
	
	i=len(binary)
	output = ""
	while i>=0:
		if i-6 < 0 :
			while len(binary)!=6:
				binary = '0' + binary
			if binary != "000000":
				output = binary_to_base64(binary) + output
			i=-1
		else:
			output = binary_to_base64(binary[i-6:i]) + output
			binary = binary[:i-6]
			i = i-6
	return output

string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
print(hex_to_base64(string))
