import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from statistics import mean 
from preprocess import *


x_train, y_train , x_test, y_test = preprocess()

ones_col = np.ones([len(x_train),1])
x_train = np.hstack((ones_col,x_train))						# ones are appended to each training example, for Wo 

ones_col_test = np.ones([len(x_test),1])
x_test = np.hstack((ones_col_test,x_test))					# same is done for test examples

w = np.zeros((1,len(x_train[0])))							# weight matrix initialised with zeroes

epochs = 1
alpha = 0.00001
num_sv = []													# number of support vectors
tn_acc =[]													# train accuracy
t_acc = []													# test accuracy
ep = []
total_epochs = 500

while(epochs < total_epochs):
	y= np.multiply(w,x_train)
	y = (np.sum(y,axis=1)).reshape(-1,1)
	sv = 0
	for i in range(len(y)):
		if(y_train[i,0]==1 and y[i,0]<=1):
			sv += 1
		elif(y_train[i,0]==-1 and y[i,0]>= -1):
			sv += 1

	num_sv.append(sv)
	D = np.subtract(y,y_train)
	err =  ((np.dot(D.transpose(),D))/len(y))[0,0]
	prod = y * y_train
	count = 0
	lambda_svm = 0.00001										# lambda 
	
	for val in prod:
		if(val >= 1):
		    cost = 0
		    w = w - alpha * (2 * lambda_svm * w)				# weight update
		
		else:
			cost = 1 - val 
			w = w + alpha * (x_train[count] * y_train[count] - 2 * lambda_svm * w)
		
		count += 1
	
	y_pred = np.multiply(w,x_test)
	y_pred = (np.sum(y_pred,axis=1)).reshape(-1,1)
	
	test_correct = 0
	for k in range(len(y_pred)):
		if(y_pred[k,0] >=0):
			y_pred[k,0] = 1
			if(y_test[k,0]==1):
				test_correct += 1
			
		else:
			y_pred[k,0] = -1
			if(y_test[k,0]== -1):
				test_correct += 1
	
	test_acc = float(test_correct*100)/len(y_test)							# test accuracy
	t_acc.append(test_acc)
	
	y_pred_train = np.multiply(w,x_train)
	y_pred_train = (np.sum(y_pred_train,axis=1)).reshape(-1,1)
	
	train_correct = 0
	for k in range(len(y_pred_train)):
		if(y_pred_train[k,0] >=0):
			y_pred_train[k,0] = 1
			if(y_train[k,0]==1):
				train_correct += 1
			
		else:
			y_pred_train[k,0] = -1
			if(y_train[k,0]== -1):
				train_correct += 1
	
	train_acc = float(train_correct*100)/len(y_train)						# train accuracy
	tn_acc.append(train_acc)
	ep.append(epochs)
	print(str(epochs)+" "+str(train_acc)+" "+str(test_acc)+ " "+str(sv))
	epochs += 1

axes = plt.gca()
axes.set_xlim([0,epochs+10])
axes.set_ylim([0,100])	
plt.plot(ep , tn_acc , 'b' , label = "Train accuracy" )
plt.plot(ep , t_acc , 'r' , label = "Test accuracy" )						# plot accuracy v/s iterations
plt.title("Accuracy" )
plt.legend(loc='lower right')
plt.xlabel("Number of iterations")
plt.ylabel('Accuracy')
plt.savefig("acc.png" )
plt.close()


axes = plt.gca()
axes.set_xlim([0,epochs+10])
axes.set_ylim([0,len(x_train) + 10])	
plt.plot(ep , num_sv , 'r' , label = "Number of Support Vectors" )			# plot number of support vectors v/s iterations
plt.title("Number of Support Vectors" )
plt.legend(loc='lower right')
plt.xlabel("Number of iterations")
plt.ylabel('Number of Support Vectors')
plt.savefig("SupportVec.png" )
plt.close()
