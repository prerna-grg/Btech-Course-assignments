import numpy
import pandas as pd
import math
from numpy import linalg as LA
from numpy.linalg import inv
import pickle
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# transforms the features into their non linear combinations 
# Eg. degree = 2
# output = 1 , x1 , x2 , x1^2 , x2^2 , x1x2
def featuretransform(X,degree):
	new_X = dict() # new input matrix
	pow_i = 0 # initialisation
	pow_j = 0 # initialisation
	i=0 
	while pow_i+pow_j <= degree:
		a = X[:,0] # x1
		while pow_i+pow_j <= degree:
			b = X[:,1] # x2
			new_X[i] = ( numpy.multiply( numpy.power(a,pow_i) , numpy.power(b,pow_j) ) ) # (x1^pow_i) * (x2^pow_j)
			pow_j +=1
			i+=1
		pow_i+=1
		pow_j=0
	frame = pd.DataFrame.from_dict(new_X) # convert the matrix to a dataframe and return
	return frame


# Plots the contour plot as learned by the code
def plotdecisionboundary(W, data, name , degree , means , stds ):
	u = numpy.linspace(1, 5, 40) # choose 40 points on x-axis between 1 and 5
	v = numpy.linspace(2, 7, 40) # choose 40 points on x-axis between 2 and 7
	z = numpy.zeros([len(u), len(v)]) 
	for i in range(len(u)):
		for j in range(len(v)):
			x = featuretransform(numpy.array([u[i], v[j]]).T.reshape(1,2).astype(numpy.float32), degree ) # apply feature transform
			x = getStandardizedTestData(x , means , stds ) # standardize using means and standard deviation of the training data set
			z[i, j] = numpy.matmul(x, W) # find the output and store
	z = z.T
	approved = data[numpy.where(data[:, 2]==1)] # mark the positive labels 
	declined = data[numpy.where(data[:, 2]==0)] # mark the negative labels
	plt.scatter(approved[:, 0], approved[:, 1], c = 'b', label='credit approved')
	plt.scatter(declined[:, 0], declined[:, 1], c = 'r', label='credit unapproved')
	plt.legend(loc='upper left')
	plt.xlabel("Attr 1")
	plt.ylabel('Attr 2')
	plt.contour(u, v, z, 0)
	plt.savefig(name)
	plt.close()


# return the percentage of incorrect labels 
def getAccuracy(A,B):
	for i in range(len(A)):
		if A[i]<0.5: # round off to get proper predicted labels
			A[i] = 0
		else:
			A[i] = 1
	err = 0
	for i in range(len(A)):
		if A[i]!=B[i]:
			err+=1
	return 100-float(err*100/len(B)) # 100 - number of wrong labels/total number


# calculates 1/1+e^(-wTX)
def mylogridgeregeval( X , W ):
	return 1/(numpy.exp(numpy.dot(-X,W)) + 1)


# calculates the error between 2 vectors using y[i]*log(f(x[i])) + (1-y[i])*(1-log(1-f(x(i)))
def logistic_error(A,B):
	if len(A) != len(B):
		print("::: Cannot calculate Mean Squared Error")
		return -1
	err = 0
	for i in range(len(A)):
		if A[i] == 0:
			if B[i]!=0:
				err += 1
		elif A[i] == 1:
			if B[i]!=1:
				err += 1
		else:
			err -= B[i]*math.log(A[i],2.73) + (1-B[i])*math.log(1-A[i] , 2.73)
	return err
		

# Regularized Gradient Descent
def gradientDescent(X , Y , _lambda ):
	alpha = 0.00009 # learning rate
	W = numpy.random.rand(len(X[0]),1) 
	itrr = 1000 # Number of iterations
	i=0
	for x in range(len(X[0])):
		W[x][0] = numpy.random.randint(0,1) # random initialisation
	while True:
		FX = mylogridgeregeval(X,W) # calculates f(x)
		err_ = logistic_error( FX , Y )  # calculate the error
		if i == itrr:
			break
		W = W - (alpha*_lambda*2)*numpy.array(W) - (alpha)*numpy.array( numpy.matmul(X.T , FX-Y) )  # update the learning matrix
		i+=1
	return W,err_


# Newton Raphson method to learn models
def newtonRaphson(X , Y , _lambda ):
	W = numpy.random.rand(len(X[0]),1)
	err_ = 0
	itr = 20 # number of iterations
	itrr =0
	out = []
	for x in range(len(X[0])):
		W[x][0] = numpy.random.uniform(-0.1,0.1) # random initialisation
	while True:
		itrr+=1
		FX = mylogridgeregeval(X,W) # calculates f(x)
		err = logistic_error( FX , Y ) # calculates error
		if itrr >= itr:
			err_ = err
			break
		R = numpy.identity(len(X)) # initialise the R matrix
		for i in range(len(X)):
			R[i][i] = FX[i] * (1-FX[i])
		A = inv( numpy.matmul( numpy.matmul(X.T , R ) , X ) + 2*_lambda*(numpy.identity(len(W))) )
		B = (_lambda*2)*numpy.array(W) + numpy.array( numpy.matmul(X.T , FX-Y) ) 
		W = W - numpy.matmul( A , B ) # update the learning matrix
	return W,err_


# Standarize the test data using mean and standard deviations obtained from the train data
def getStandardizedTestData(data , means , stds ):
	for i in data.columns:
		mean = means[i]
		std = stds[i]
		#if std=0 just ignore because all values are same
		if std!=0:
			data.loc[:,i] -= mean
			data.loc[:,i] /= std
	return data


# standardize the train data by calculating the mean and standard deviation column wise
def getStandardizedTrainData(data):
	means = dict()
	stds = dict()
	for i in data.columns:
		mean = data[i].mean()
		std = data[i].std()
		means[i] = mean
		stds[i] = std
		if std!=0:
			data.loc[:,i] -= mean
			data.loc[:,i] /= std
	return data,means,stds


# fr% data goes to test set
# remaining is put back into the train sets
def getRandomData(data , fr ):
	test = data.sample(frac=fr)
	train = data.loc[~data.index.isin(test.index)]
	return train , test	


# caller for logistic regression
def run_logisitc_reg(fraction , lambda_ , degree ):
	if degree<0:
		degree = 0
	output = []
	data = pd.read_csv("credit.txt" , header=None)
	
	if len(data.columns)!=3:
		print ("Data configuration error")
		exit()
	train , test  = getRandomData(data , fraction )
	for_plot = train.values
	age_Y = train[2]
	age_Y_t = test[2]
	del train[2]
	del test[2]
	
	train = featuretransform ( train.values , degree ) # transform the features
	test =  featuretransform ( test.values , degree ) # transform the features
	train , means , stds = getStandardizedTrainData(train) # standardize the train data
	test = getStandardizedTestData(test , means , stds ) # standardize the test data
	train = train.values # convert to numpy array
	age_Y= age_Y.values # convert to numpy array
	age_Y = age_Y.reshape((len(age_Y),1)) # convert to (n,) to (n,1)

	test = test.values # convert to numpy array
	age_Y_t = age_Y_t.values # convert to numpy array
	age_Y_t = age_Y_t.reshape((len(age_Y_t),1)) # convert to (n,) to (n,1)

	W,err = newtonRaphson(train , age_Y , float(lambda_) ) # find the learned model
	# Plot the decision contour
	plotdecisionboundary(W , for_plot , "D:" + str(degree) + "_l:" + str(lambda_) + "_fr:" + str(fraction)+ ".png" , degree , means , stds )
	acc_train = getAccuracy( mylogridgeregeval(train,W) , age_Y ) # return the train error
	acc_test =  getAccuracy( mylogridgeregeval(test,W) , age_Y_t ) # return the test error
		
	return acc_train , acc_test

if __name__ =="__main__":
	pd.options.mode.chained_assignment = None
	lambda_ = [0.01 , 0.02 , 0.05 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 ]
	fractions = [0.50 , 0.40 , 0.30 , 0.20 , 0.10 ] 
	degrees = [ 1 , 2 , 3, 4 , 5 , 6 ]
	
	for l in lambda_:
		for f in fractions:
			train = []
			test = []
			for i in range(len(degrees)):
				print ( "Running for lambda = " + str(l) + " Fraction = " + str(f) + " Degree = " + str(degrees[i]) )
				a = []
				b = []
				for n in range(1):
					a1,b1 = run_logisitc_reg(  f , l ,  degrees[i] )
					a.append(a1)
					b.append(b1)
				train.append( numpy.mean(numpy.array(a)))
				test.append( numpy.mean(numpy.array(b)))
		
			plt.title( 'Degree Analysis for Lambda = ' + str(l) + " Train set fraction = " + str(1-f) )
			plt.xlabel('Degree')
			plt.ylabel('Accuracy')
			plt.plot( degrees , train , 'b' )
			plt.plot( degrees , test , 'r' )
			plt.savefig("L:" +str(l) + "_fr:" + str(f) + ".png") 
			plt.close()
	
