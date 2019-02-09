import numpy
import pandas as pd
import math
from numpy import linalg as LA
from numpy.linalg import inv
import pickle
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from preprocess import *

# return the percentage of incorrect labels 
def getAccuracy(A,B):
	for i in range(len(A)):
		if A[i]<0.5: # round off to get proper predicted labels
			A[i] = 0
		else:
			A[i] = 1
	corr = 0
	for i in range(len(A)):
		if A[i]==B[i]:
			corr+=1
	return 100.0*corr/len(A)


# calculates 1/1+e^(-wTX)
def mylogridgeregeval( X , W ):
	return 1/(numpy.exp(numpy.dot(-X,W)) + 1)

# caller for logistic regression
def run_logisitc_reg(alpha , _lambda):
	output = []
	X_train , y_train , X_test , y_test = preprocess()
	
	for i in range(len(y_train)):
		if y_train[i] == -1:
			y_train[i] = 0
	for i in range(len(y_test)):
		if y_test[i] == -1:
			y_test[i] = 0
	
	W = numpy.random.rand(len(X_train[0]),1) 
	itrr = 1500 # Number of iterations
	i=0
	for x in range(len(X_train[0])):
		W[x][0] = numpy.random.randint(-1,1) # random initialisation
		
	tn_acc = []
	ts_acc = []
	while True:
		FX = mylogridgeregeval(X_train,W) # calculates f(x)
		acc = getAccuracy( FX , y_train )  # calculate the acc
		FX_t = mylogridgeregeval(X_test,W) # calculates f(x)
		acc_t = getAccuracy( FX_t , y_test )  # calculate the acc
		print( i , acc , acc_t )
		tn_acc.append(acc)
		ts_acc.append(acc_t)
		if i >= itrr:
			break
		W = W - (alpha*_lambda*2)*numpy.array(W) - (alpha)*numpy.array( numpy.matmul(X_train.T , FX-y_train) )  # update the learning matrix
		i+=1
		
	
	x = range(itrr+1)
	axes = plt.gca()
	axes.set_xlim([0,itrr+10])
	axes.set_ylim([0,100])
	plt.plot(x , tn_acc , 'b' , label = "Train accuracy" )
	plt.plot(x , ts_acc , 'r' , label = "Test accuracy" )
	plt.title("Accuracy" )
	plt.legend(loc='upper left')
	plt.xlabel("Number of iterations")
	plt.ylabel('Accuracy')
	plt.savefig("log_reg" + str(alpha) + "_" + str(_lambda) + ".png") 
	plt.close()
	acc_train = getAccuracy( mylogridgeregeval(X_train,W) , y_train ) # return the train error
	acc_test =  getAccuracy( mylogridgeregeval(X_test,W) , y_test ) # return the test error
	return acc_train , acc_test

if __name__ =="__main__":
	pd.options.mode.chained_assignment = None
	a1,b1 = run_logisitc_reg(  0.00001 , 0.0001 )
	print ( a1 , b1 )
