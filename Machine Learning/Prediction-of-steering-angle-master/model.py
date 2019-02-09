import os
import sys
import cv2
import glob
import math
import scipy
import pickle
from scipy.special import expit
import random  
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Stable Sigmoid Activation Function
def sigmoid(x):
	return scipy.special.expit(x)


# Class to hold everything of neural network
class NeuralNetwork:
	def __init__(self , num , alpha):
		self.drop_flag = 0 # initialisation
		self.Adam_opt = 0 # initialisation
		self.alpha = alpha # parameter
		gap = (0.02/num)/512 # parameter
		self.w1 = np.random.uniform( -0.01 , 0.01 , ( num , 512) )
		c = 0
		# uniform spacing in weight matrices
		for i in range(len(self.w1)):
			for j in range(len(self.w1[0])):
				if i==0:
					self.w1[i][j] = 0
				else :
					self.w1[i][j] = -0.01 + gap * c
					c += 1
		gap = (0.02/512)/64
		self.w2 = np.random.uniform( -0.01 , 0.01 , (513 , 64) )
		c = 0
		# uniform spacing in weight matrices
		for i in range(len(self.w2)):
			for j in range(len(self.w2[0])):
				if i==0:
					self.w1[i][j] = 0
				else :
					self.w2[i][j] = -0.01 + gap * c
					c += 1
		gap = 0.02/64
		self.w3 = np.random.uniform( -0.01 , 0.01 , ( 65 ,1 ) )
		c = 0
		# uniform spacing in weight matrices
		for i in range(len(self.w3)):
			for j in range(len(self.w3[0])):
				if i==0:
					self.w1[i][j] = 0
				else :
					self.w3[i][j] = -0.01 + gap * c
					c += 1

	# set the input to be served in next iteration
	def miniBatchInput(self , x , y):
		self.X = x
		self.Y = y
	
	
	# 0s and 1s matrices in dropout
	def drop_matrix(self,X,percentage):
		(n,m) = X.shape
		zeros = int(percentage*m)
		rand_list = random.sample(range(0,m), int(zeros))
		drop_matrix = np.ones((n,m))
		for i in rand_list:
			drop_matrix[:,i] = 0
		return drop_matrix

	
	def forwardProp(self):
		if self.drop_flag == 1:
			self.X = np.multiply( self.drop_matrix(self.X,self.frac1) , self.X ) # multiply the input by ones and zeros created
			self.O1 = sigmoid(np.dot(self.X , self.w1))
			self.m1 = self.drop_matrix(self.O1,self.frac2) # save the dropout state for back propagation
			self.O1 = np.multiply( self.O1 , self.m1 )  # multiply the hidden layer by ones and zeros matrix
			self.P1 = np.multiply(self.O1, 1- self.O1).T
			self.O1 = np.append(np.ones((len(self.O1),1)) , self.O1 , axis = 1)
			self.O2 = sigmoid(np.dot(self.O1,self.w2))
			self.m2 = self.drop_matrix(self.O2,self.frac3)# save the dropout state for back propagation
			self.O2 = np.multiply( self.O2 , self.m2 )# multiply the hidden layer by ones and zeros matrix
			self.P2 = np.multiply(self.O2, 1- self.O2).T
			self.O2 = np.append(np.ones((len(self.O2),1)) , self.O2 , axis = 1)
			self.O3 = np.dot(self.O2,self.w3)
		else:
			self.O1 = sigmoid( np.dot( self.X , self.w1 ) ) # output is N x 512
			self.P1 = np.multiply( self.O1 , 1-self.O1 ).T # pass
			bias = np.ones(( len(self.O1), 1)) # bias
			self.O1 = np.append( bias, self.O1 , axis = 1 ) # appending the bias
			self.O2 = sigmoid( np.dot( self.O1 , self.w2 ) ) # output is N x 64
			self.P2 = np.multiply( self.O2 , 1-self.O2 ).T # pass
			bias = np.ones(( len(self.O2), 1)) # bias
			self.O2 = np.append( bias, self.O2 , axis = 1 ) # appending the bias
			self.O3 = np.dot( self.O2 , self.w3 ) # output is N x 1

	def backwardProp(self):
		self.D3 = ( self.O3 - self.Y ).T # output is 1 x N 
		# reducing the step gradient for larger parameters
		if (len(self.D3[0]) > 100 and self.alpha>=0.006) or (len(self.D3[0]) > 50 and self.alpha>=0.01):
			self.D3 = self.D3 / len(self.Y)
		self.D2 = np.multiply ( np.dot ( self.w3[1:,:] , self.D3 ) , self.P2 ) # differential
		if self.drop_flag==1 :
			self.D2 = np.multiply( self.D2.T , self.m2 ).T # multiply by drop out matrix 
		self.D1 = np.multiply ( np.dot ( self.w2[1:,:] , self.D2 ) , self.P1 ) # differential
		if self.drop_flag==1 :
			self.D1 = np.multiply( self.D1.T , self.m1 ).T # multiply by drop out matrix 
		# update the weights with the derivative (slope) of the loss function
		dw3 = np.dot( self.D3 , self.O2 ).T # gradient in weight matrix 1
		dw2 = np.dot( self.D2 , self.O1 ).T # gradient in weight matrix 2
		dw1 = np.dot( self.D1 , self.X ).T # gradient in weight matrix 3
		
		# adam optimisation
		if self.Adam_opt == 1:
			self.t += 1
			self.mt3 = self.beta1*self.mt3 + (1-self.beta1)*dw3
			self.mt2 = self.beta1*self.mt2 + (1-self.beta1)*dw2
			self.mt1 = self.beta1*self.mt1 + (1-self.beta1)*dw1
			self.vt3 = self.beta2*self.vt3 + (1-self.beta2)*( np.multiply(dw3 , dw3))
			self.vt2 = self.beta2*self.vt2 + (1-self.beta2)*( np.multiply(dw2 , dw2))
			self.vt1 = self.beta2*self.vt1 + (1-self.beta2)*( np.multiply(dw1 , dw1))
			mt3c = ((1- self.beta1**self.t)**-1)*self.mt3
			mt2c = ((1- self.beta1**self.t)**-1)*self.mt2
			mt1c = ((1- self.beta1**self.t)**-1)*self.mt1
			vt3c = (((1- self.beta2**self.t)**-1)*self.vt3)**0.5 + self.e
			vt2c = (((1- self.beta2**self.t)**-1)*self.vt2)**0.5 + self.e
			vt1c = (((1- self.beta2**self.t)**-1)*self.vt1)**0.5 + self.e
			self.w3 -= self.alpha * ( mt3c / vt3c )
			self.w2 -= self.alpha * ( mt2c / vt2c )
			self.w1 -= self.alpha * ( mt1c / vt1c )
		else:
			self.w3 -= self.alpha*dw3
			self.w2 -= self.alpha*dw2
			self.w1 -= self.alpha*dw1
					
	def DropOutLayer(self , frac1 , frac2 , frac3 ):
		self.drop_flag = 1 # inform others about dropout
		if frac1!=0 or frac2!=0 or frac3!=0:
			self.drop_flag = 1
			self.frac1 = frac1
			self.frac2 = frac2
			self.frac3 = frac3
		K = int(round(1024 * frac1))
		self.Dw1 = np.array( [0]*K + [1]*(1024-K) )
		np.random.shuffle(self.Dw1) # dropout vector
		self.Dw1 = self.Dw1.reshape(len(self.Dw1),1)
		self.Dw1 = np.append( np.ones((1,1)) , self.Dw1 , axis = 0 )
		self.Dw1 = self.Dw1.reshape(len(self.Dw1),1)
		self.Dw1 = self.Dw1.T
		K = int(round(512 * frac2))
		self.Dw2 = np.array( [0]*K + [1]*(512-K) )
		np.random.shuffle(self.Dw2) # dropout vector
		self.Dw2 = self.Dw2.reshape(len(self.Dw2),1).T
		K = int(round(64 * frac2))
		self.Dw3 = np.array( [0]*K + [1]*(64-K) )
		np.random.shuffle(self.Dw3) # dropout vector
		self.Dw3 = self.Dw3.reshape(len(self.Dw3),1).T
	
	
	# Initialisations for Adam optimizer
	def Adam_Optimizer(self):
		self.Adam_opt = 1
		self.gt1 = np.zeros( (self.w1.shape))
		self.gt2 = np.zeros( (self.w2.shape))
		self.gt3 = np.zeros( (self.w3.shape))
		self.mt1 = np.zeros( (self.w1.shape))
		self.mt2 = np.zeros( (self.w2.shape))
		self.mt3 = np.zeros( (self.w3.shape))
		self.vt1 = np.zeros( (self.w1.shape))
		self.vt2 = np.zeros( (self.w2.shape))
		self.vt3 = np.zeros( (self.w3.shape))
		self.e = 10**-8
		self.beta1 = 0.9
		self.beta2 = 0.999
		self.t = 0
	
	def trainAccuracy(self):
		return np.sum ( np.square( np.subtract ( self.O3 , self.Y ) ) )/(2*len(self.X)))
		
	def testAccuracy(self,x,y):
		o1 = self.frac2*sigmoid( np.dot( self.frac1*x , self.w1 ) ) # output is N x 512
		bias = np.ones(( len(o1), 1))
		o1 = np.append( bias, o1 , axis = 1 ) # output is N x 512
		o2 = self.frac3*sigmoid( np.dot( o1 , self.w2 ) ) # output is N x 64
		bias = np.ones(( len(o2), 1))
		o2 = np.append( bias, o2 , axis = 1 ) # output is N x 64
		o3 = np.dot( o2 , self.w3 ) # output is N x 1
		return np.sum ( np.square( np.subtract ( o3 , y ) ) )/(2*len(x))


# changes the image from 3 rgb channels to 1 gray channel
def rgb2gray(rgb):
    if len(rgb.shape) is 3:
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    else:
        print ('Current image is already in grayscale.')
        return rgb


# standardizes the test data with means and standard deviations obtained from the train data
def getStandardizedTestData(data , means , stds):
	for i in range(len(data[0])):
		mean = means[i]
		std = stds[i]
		data[:,i] = data[:,i] - mean
		if std!=0:
			data[:,i] = data[:,i] / std
	return data


# standardizes the train data
def getStandardizedTrainData(data):
	means = []
	stds = []
	for i in range(len(data[0])):
		mean = data[:,i].mean()
		means.append(mean)
		std = data[:,i].std()
		stds.append(std)
		data[:,i] = data[:,i] - mean
		if std!=0:
			data[:,i] = data[:,i] / std
	return data,means,stds


# Read the folder and get images to create feature vector
def load_data(folder , labels ):
	gray_images = {}
	print ( "Reading Images ... " )
	gg =0 
	for file_ in glob.glob("steering/*.jpg"):
		my_img = cv2.imread(file_)
		gray_images[file_.split("/")[1]] = rgb2gray(my_img).ravel()

	train_X = []
	train_Y = []
	test_X = []
	test_Y = []
	limit = round(len(labels)*0.8)
	for i in range( limit ):
		train_X.append( gray_images[labels[0][i].split("/")[1]] )
		train_Y.append( labels[1][i] )
	for i in range( limit , len(labels) ):
		test_X.append( gray_images[labels[0][i].split("/")[1]] )
		test_Y.append( labels[1][i] )
	print ( "Feature vectors generated" )
	return np.array(train_X) , np.array(train_Y).reshape(len(train_Y),1) , np.array(test_X) , np.array(test_Y).reshape(len(test_Y),1)


# Main function for a single neural network
def Run_Neural_Network(iterations , alpha , mini_b_size , train_X , train_Y , test_X , test_Y , f1=0 , f2=0 , f3=0 ):
	adam_flag = 0
	if f1 == "adam":
		adam_flag =1
		print("Adam Optimisation = True" )
		f1 = 0
	print("\nNumber of iterations= " + str(iterations))
	print("Alpha = " + str(alpha))
	print("Mini Batch Size = " + str(mini_b_size))
	drop_out = 0
	if f1!=0 or f2!=0 or f3!=0:
		print("Dropout = True" )
		drop_out = 1
	else:
		print("Dropout = False" )
	mini_b_iter = int(math.floor( len(train_X) / mini_b_size ))
	
	train_acc = []
	test_acc = []
	if os.path.exists( str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out) + ".pkl" ):
		save_file = open ( str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out) + ".pkl" ,"rb")
		nn = pickle.load(save_file)
		save_file = open(str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out) + "_train.pkl" ,"rb")
		train_acc = pickle.load(save_file)
		print(type(train_acc))
		save_file = open( str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out) + "_test.pkl","rb")
		test_acc = pickle.load(save_file)
	else:
		nn = NeuralNetwork( train_X.shape[1] , alpha )
		if adam_flag ==1:
			nn.Adam_Optimizer()
		for i in range(iterations+1):
			# randomly shuffle the input data in every iteration
			temp = np.c_[train_X , train_Y]
			np.random.shuffle(temp)
			train_X = temp[:,:-1]
			train_Y = temp[:,-1].reshape(len(temp[:,-1]),1)
			
			# traverse the mini batches 
			for j in range(mini_b_iter):
				# if dropout is to be implemented 
				if drop_out==1:
					nn.DropOutLayer ( f1 , f2 , f3 )
				x = train_X[ j*mini_b_size : j*mini_b_size + mini_b_size ]
				y = train_Y[ j*mini_b_size : j*mini_b_size + mini_b_size ]
				nn.miniBatchInput( x , y )
				nn.forwardProp()
				nn.backwardProp()
			nn.miniBatchInput( train_X[ mini_b_iter*mini_b_size : len(train_X) ] , train_Y[ mini_b_iter*mini_b_size : len(train_Y) ] )
			nn.forwardProp()
			nn.backwardProp()
			
			# calculate the errors and save the result
			x = train_X
			y = train_Y
			nn.miniBatchInput( x , y )
			nn.forwardProp()
			a = nn.trainAccuracy()
			train_acc.append( a )
			b = nn.testAccuracy( test_X , test_Y )
			test_acc.append( b )
			print ( "Iteration = " + str(i) + " : " + str(a) + " " + str(b) )
			
		# save the results in pickle files
		my_str = str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out)
		if adam_flag ==1:
			my_str += "_adam"
		save_file = open( my_str + ".pkl" ,"wb") # save the model
		pickle.dump(nn,save_file)
		save_file.close()
		save_file = open( my_str + "_train.pkl","wb") # save the model
		pickle.dump(train_acc,save_file)
		save_file.close()
		save_file = open( my_str + "_test.pkl","wb") # save the model
		pickle.dump(test_acc,save_file)
		save_file.close()
	
	# plot everything
	x = range(iterations+1)
	axes = plt.gca()
	axes.set_xlim([0,iterations+10])
	axes.set_ylim([0,0.5])
	plt.plot(x , train_acc , 'b' , label = "Train error" )
	plt.plot(x , test_acc , 'r' , label = "Test error" )
	plt.title("Mean Square Error" )
	plt.legend(loc='upper left')
	plt.xlabel("Number of iterations")
	plt.ylabel('Mean Squared Error')
	plt.savefig( my_str + ".png" )
	plt.close()
	
	
if __name__ =="__main__":
	pd.options.mode.chained_assignment = None
	data = pd.read_csv("steering/data.txt" , header=None , delim_whitespace=True)
	data = data.sample(frac=1).reset_index(drop=True)
	print("Size of data = " + str(len(data)))
	train_X , train_Y , test_X , test_Y = load_data("steering/*.jpg" , data )
	
	# Standardize the inputs
	train_X,means,stds = getStandardizedTrainData(train_X)
	test_X = getStandardizedTestData(test_X , means , stds)
	
	# append 1 to account for bias term
	bias = np.ones(( len(train_X), 1))
	train_X = np.append( bias, train_X , axis = 1 )
	bias = np.ones(( len(test_X), 1))
	test_X = np.append( bias, test_X , axis = 1 )
	
	# task 1
	#Run_Neural_Network( 5000 , 0.01 , 64 , train_X , train_Y , test_X , test_Y)
	
	# task 2
	#Run_Neural_Network( 1000 , 0.01 , 32 , train_X , train_Y , test_X , test_Y)
	#Run_Neural_Network( 1000 , 0.01 , 64 , train_X , train_Y , test_X , test_Y)
	#Run_Neural_Network( 1000 , 0.01 , 128 , train_X , train_Y , test_X , test_Y)
	
	# task 3
	#Run_Neural_Network( 1000 , 0.001 , 32 , train_X , train_Y , test_X , test_Y , 0.5 , 0.5 , 0.5 )
	#Run_Neural_Network( 1000 , 0.001 , 64 , train_X , train_Y , test_X , test_Y , 0.5 , 0.5 , 0.5 )
	#Run_Neural_Network( 1000 , 0.001 , 128 , train_X , train_Y , test_X , test_Y , 0.5 , 0.5 , 0.5  )
	
	# task 4
	#Run_Neural_Network( 1000 , 0.05 , 64 , train_X , train_Y , test_X , test_Y)
	#Run_Neural_Network( 1000 , 0.005 , 64 , train_X , train_Y , test_X , test_Y)	
	#Run_Neural_Network( 1000 , 0.001 , 64 , train_X , train_Y , test_X , test_Y)
	
	# task 5 
	Run_Neural_Network( 100 , 0.005 , 128 , train_X , train_Y , test_X , test_Y , "adam" )
	Run_Neural_Network( 300 , 0.005 , 128 , train_X , train_Y , test_X , test_Y)

