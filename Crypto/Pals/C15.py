def PKCS7_unpadding(text):
	last = text[-1]
	for i in range(last):
		if text[-1] != last:
			return ('Invalid Padding')
		text = text[:-1]
	return text
	
print(PKCS7_unpadding(b"ICE ICE BABY\x04\x04\x04\x04"))
print(PKCS7_unpadding(b"ICE ICE BABY\x05\x05\x05\x05"))
print(PKCS7_unpadding(b"ICE ICE BABY\x01\x02\x03\x04"))
