import os
import random

def getRandomReviews(filename_r , filename_w , rev_req ):
	rev_req = int( rev_req/2)
	feature_file = open( filename_r , "r")
	f1 = feature_file.readlines() # feature vectors for reviews
	num_lines = 0
	all_lines = []
	pos_lines = []
	neg_lines = []
	pos_rev = [] #randomly selected
	neg_rev = [] #randomly selected
	for line in f1:
		num_lines +=1
		all_lines.append(line)
	
	for i in range(int(num_lines/2)):
		pos_lines.append(all_lines[i])
		
	for i in range(int(num_lines/2)):
		neg_lines.append(all_lines[int(num_lines/2) + i])
	
	random.shuffle(pos_lines)
	random.shuffle(neg_lines)

	my_rev = open(filename_w, "a")
	for i in pos_lines[:rev_req]:
		my_rev.write(str(i))
		
	for i in neg_lines[:rev_req]:
		my_rev.write(str(i))
	
	my_rev.close()

if __name__ =="__main__":
	if os.path.exists("data.txt"):
		os.remove("data.txt")
	#a = open("data.txt" , "a")
	#a.close()
	getRandomReviews("../project1/aclImdb/train/labeledBow.feat" , "data.txt" , 1000 )
	getRandomReviews("../project1/aclImdb/test/labeledBow.feat" , "data.txt" , 1000 )
	
