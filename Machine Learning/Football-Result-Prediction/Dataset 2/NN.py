import os
import sys
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
 #!/usr/bin/env python -W ignore::DeprecationWarning
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from time import time 
from sklearn.metrics import f1_score
from preprocess import *

# Stable Sigmoid Activation Function
def sigmoid(x):
	x = np.float64(x)
	return scipy.special.expit(x)

# Class to hold everything of neural network
class NeuralNetwork:
	def __init__(self , num0 , num1 , num2 , alpha):
		self.drop_flag = 0 # initialisation
		self.Adam_opt = 0 # initialisation
		self.alpha = alpha # parameter
		self.frac1 = self.frac2 = self.frac3 = 1
		self.w1 = np.random.uniform( -0.01 , 0.01 , ( num0 , num1 ) )
		self.w2 = np.random.uniform( -0.01 , 0.01 , ( (num1+1) , num2) )
		self.w3 = np.random.uniform( -0.01 , 0.01 , ( (num2+1) ,1 ) )

	# set the input to be served in next iteration
	def miniBatchInput(self , x , y):
		self.X = x
		self.Y = y

	def forwardProp(self):
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
		#print("--->" , type(self.Y[0][0]))
		self.D3 = ( self.O3 - self.Y ).T # output is 1 x N 
		self.D2 = np.multiply ( np.dot ( self.w3[1:,:] , self.D3 ) , self.P2 ) # differential
		self.D1 = np.multiply ( np.dot ( self.w2[1:,:] , self.D2 ) , self.P1 ) # differential
		dw3 = np.dot( self.D3 , self.O2 ).T # gradient in weight matrix 1
		dw2 = np.dot( self.D2 , self.O1 ).T # gradient in weight matrix 2
		dw1 = np.dot( self.D1 , self.X ).T # gradient in weight matrix 3
		dw3 = dw3.astype(np.float64)
		dw2 = dw2.astype(np.float64)
		dw1 = dw1.astype(np.float64)
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
			#print ( type(self.w3[0][0]))
			#print ( type(dw3[0][0]))
			#print (dw3)
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

	def testAccuracy(self,x,y):
		o1 = self.frac2*sigmoid( np.dot( self.frac1*x , self.w1 ) ) # output is N x 512
		bias = np.ones(( len(o1), 1))
		o1 = np.append( bias, o1 , axis = 1 ) # output is N x 512
		o2 = self.frac3*sigmoid( np.dot( o1 , self.w2 ) ) # output is N x 64
		bias = np.ones(( len(o2), 1))
		o2 = np.append( bias, o2 , axis = 1 ) # output is N x 64
		o3 = np.dot( o2 , self.w3 ) # output is N x 1
		return np.sum ( np.square( np.subtract ( o3 , y ) ) )/(len(x))
		
	def testAccuracy2(self,x,y):
		o1 = self.frac2*sigmoid( np.dot( self.frac1*x , self.w1 ) ) # output is N x 512
		bias = np.ones(( len(o1), 1))
		o1 = np.append( bias, o1 , axis = 1 ) # output is N x 512
		o2 = self.frac3*sigmoid( np.dot( o1 , self.w2 ) ) # output is N x 64
		bias = np.ones(( len(o2), 1))
		o2 = np.append( bias, o2 , axis = 1 ) # output is N x 64
		o3 = np.dot( o2 , self.w3 ) # output is N x 1
		om = np.dot( o2 , self.w3 ) # output is N x 1
		for i in range(len(o3)):
			if o3[i] < 0:
				om[i] = -1
			else:
				om[i] = 1
		corr = 0
		for i in range(len(om)):
			if om[i] == y[i]:
				corr+=1
		return (100.0*corr)/(len(x))
	

# Main function for a single neural network
def Run_Neural_Network(iterations , alpha , mini_b_size , train_X , train_Y , test_X , test_Y , num0 , num1 , num2 , f1=0 , f2=0 , f3=0 ):
	adam_flag = 0
	print(type(train_Y[0][0]))
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
	tr_Acc = []
	ts_Acc = []
	my_str = str(iterations) + "_" + str(alpha) + "_"+ str(mini_b_size) + "_" + str(drop_out) + "_" + str(num1) + "_" + str(num2)
	nn = NeuralNetwork( num0 , num1 , num2  , alpha )
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
			x = x.astype(np.float64)
			y = y.astype(np.float64)
			#print(type(y[0][0]))
			nn.miniBatchInput( x , y )
			nn.forwardProp()
			nn.backwardProp()
		nn.miniBatchInput( train_X[ mini_b_iter*mini_b_size : len(train_X) ] , train_Y[ mini_b_iter*mini_b_size : len(train_Y) ] )
		nn.forwardProp()
		nn.backwardProp()
		
		# calculate the mean sqaure errors and save the result
		x = train_X
		y = train_Y
		x = x.astype(np.float64)
		y = y.astype(np.float64)
		nn.miniBatchInput( x , y )
		a = nn.testAccuracy(x,y)
		train_acc.append( a )
		b = nn.testAccuracy( test_X , test_Y )
		test_acc.append( b )
		print ( "=================================")
		print ( "Iteration = " + str(i+1) + " : " + str(a) + " " + str(b) )
		# calculate the accuracy and save the result
		x = train_X
		y = train_Y
		x = x.astype(np.float64)
		y = y.astype(np.float64)
		c = nn.testAccuracy2( x , y) 
		tr_Acc.append(c)
		print( "Train:" , c , "%")
		x = test_X
		y = test_Y
		x = x.astype(np.float64)
		y = y.astype(np.float64)
		c = nn.testAccuracy2( x , y) 
		ts_Acc.append(c)
		print("Test:" , c , "%")
			
	# plot everything
	x = range(iterations+1)
	axes = plt.gca()
	plt.plot(x , train_acc , 'b' , label = "Train error" )
	plt.plot(x , test_acc , 'r' , label = "Test error" )
	plt.title("Mean Square Error" )
	plt.legend(loc='upper left')
	plt.xlabel("Number of iterations")
	plt.ylabel('Mean Squared Error')
	plt.savefig( my_str + ".png" )
	plt.close()
	
	x = range(iterations+1)
	axes = plt.gca()
	axes.set_xlim([0,iterations+10])
	axes.set_ylim([0,100])
	plt.plot(x , tr_Acc , 'b' , label = "Train Accuracy" )
	plt.plot(x , ts_Acc , 'r' , label = "Test Accuracy" )
	plt.title("Accuracy" )
	plt.legend(loc='upper left')
	plt.xlabel("Number of iterations")
	plt.ylabel('Accuracy')
	plt.savefig( my_str + "_%_.png" )
	plt.close()
	
	
if __name__ =="__main__":
	if len(sys.argv) != 3:
		print( "Usage: python3 NN.py <num1> <num2>")
		exit()
	num1 = int(sys.argv[1])
	num2 = int(sys.argv[2])
	X_train , y_train , X_test , y_test = preprocess()
	bias = np.ones(( len(X_train), 1))
	X_train = np.append( bias, X_train , axis = 1 )
	bias = np.ones(( len(X_test), 1))
	X_test = np.append( bias, X_test , axis = 1 )
	print ( type(y_train[0][0]))
	Run_Neural_Network( 1000 , 0.001 , 128 , X_train , y_train , X_test , y_test , len(X_train[0]) , num1 , num2)
