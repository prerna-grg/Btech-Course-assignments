from collections import defaultdict
from math import log
import operator

class NaiveBayesClassifier:

	def __init__(self , content , m):
		self.train = content
		emails = []
		
		# m*p initialisation for all possible words
		self.t_countS = defaultdict(lambda: 1)
		self.t_countNotS = defaultdict(lambda: 1)
		label = 0
		total = 0
		numSpam = 0
		total_wordsS = 0
		total_wordsNotS = 0

		# get the tokens / words and labels
		for x in content:
			tokens = x.split(" ")
			for j in range(len(tokens)):
				if j==0 :
					emails.append(tokens[j])
				elif j==1:
					if tokens[j] == 'spam':
						numSpam += 1
						label = 0
					else:
						label = 1
					total += 1
				elif j%2==0:
					if label == 0:
						total_wordsS += int(tokens[j+1]) # n0
						self.t_countS[tokens[j]] += int(tokens[j+1])
						self.t_countNotS[tokens[j]] += 0
					else:
						total_wordsNotS += int(tokens[j+1]) #n1
						self.t_countNotS[tokens[j]] += int(tokens[j+1])
						self.t_countS[tokens[j]] += 0

		#print("Number of words: " + str(len(self.t_countS.keys())))
		#print("Number of words: " + str(len(self.t_countNotS.keys())))
		
		if m<0:
			m = len(self.t_countS.keys())
		
		self.pS = numSpam/total
		self.pNotS = (total - numSpam)/total
		
		for key in self.t_countS.keys():
			self.t_countS[key] /= ( m + total_wordsS)
		
		for key in self.t_countNotS.keys():
			self.t_countNotS[key] /= ( m + total_wordsNotS)

			
	def top5Spam_NotSpam(self):

		newA = sorted(self.t_countS.items(), key=operator.itemgetter(1), reverse=True)[:5]
		print("Top 5 words responsible for spam")
		for key in newA:
			print(key)

		newB = sorted(self.t_countNotS.items(), key=operator.itemgetter(1), reverse=True)[:5]
		print("\nTop 5 words responsible for not spam")
		for key in newB:
			print(key)
		

	#runs once on training data
	def getAccuracy(self , test):
		corr = 0
		for x in test:
			pS_xi = log(self.pS)
			pNotS_xi = log(self.pNotS)
			tokens = x.split(" ")
			label = 0
			for j in range(len(tokens)):
				if j==0 :
					continue
				elif j==1:
					if tokens[j] == 'spam':
						label = 0
					else:
						label = 1
				elif j%2==0:
					a = self.t_countS[tokens[j]]
					b = self.t_countNotS[tokens[j]]
					pS_xi += int(tokens[j+1]) * log(self.t_countS[tokens[j]])
					pNotS_xi += int(tokens[j+1]) * log(self.t_countNotS[tokens[j]])
					
			plabel = 1
			if pS_xi >= pNotS_xi:
				plabel = 0
			if plabel == label:
				corr += 1
		return corr/len(test)

	
if __name__ =="__main__":

	with open("nbctrain") as f:
		train = f.readlines()
	f.close()
	train = [x.strip() for x in train]
	
	nbc = NaiveBayesClassifier( train , -1 )
	print( "P(spam) = " + str(nbc.pS ))
	print( "P(~spam) = " + str(nbc.pNotS ))
	print()
	nbc.top5Spam_NotSpam()
	print("\nTrain Accuracy : " + str(nbc.getAccuracy(train)))
	with open("nbctest") as f2:
		test = f2.readlines()
	test = [x.strip() for x in test]
	f2.close()
	print("Test Accuracy: " + str(nbc.getAccuracy(test)))
	
	
	tna = []
	tsa = []
	m = 0
	while m<3000:
		m += 10
		nbc = NaiveBayesClassifier( train , m )
		a = nbc.getAccuracy(train)
		b = nbc.getAccuracy(test)
		print( m,a,b)
		tna.append(a)
		tsa.append(b)
		
	print(tna)
	print(tsa)
