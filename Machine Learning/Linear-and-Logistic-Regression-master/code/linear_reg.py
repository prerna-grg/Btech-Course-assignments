import numpy
import pandas as pd
from numpy import linalg as LA
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys

itr = 1000 # number of iterations

# performs product of X and W to return the predicted values
def mylinridgeregeval( X , W ):
	return numpy.dot(X,W)


# calculates the mean square error between two vectors
def meansquarederr(A,B):
	if len(A) != len(B):
		print("::: Cannot calculare Mean Squared Error")
		return -1
	err = 0
	diff =A - B
	err = numpy.sum(numpy.square(diff))
	err = LA.norm(diff)*LA.norm(diff)
	return err/len(A)
		

#uses gradient descent to find W on input X , Y , and regularization parameter lambda
def mylinridgereg(X , Y , _lambda ):
	alpha = 0.00001
	W = numpy.random.rand(len(X[0]),1) 
	err_ = 0
	i=0
	for x in range(len(X[0])):
		W[x][0] = numpy.random.randint(0,1) # initialise randomly
	while True:
		i += 1
		FX = mylinridgeregeval(X,W) # find the prediction
		err = meansquarederr( FX , Y ) # find the error
		# runs for 5000 iterations
		if i == itr :
			break
		W = W - (alpha*_lambda*2)*numpy.array(W) - (alpha)*numpy.array( numpy.matmul(X.T , FX-Y) )  # update the matrix
	return W


# standardizes the test data with the given values of means and standard deviations for corresponding columns
def getStandardizedTestValData(data , means , stds ):
	for i in data.columns:
		if i==0:
			continue
		mean = means[i]
		std = stds[i]
		data.loc[:,i] -= mean
		if std!=0:
			data.loc[:,i] /= std
	return data
	

# standardizes the train data with the means and standard deviations for corresponding columns
def getStandardizedTrainData(data):
	means = dict()
	stds = dict()
	for i in data.columns:
		if i==0:
			means[i] = 0
			stds[i] = 0
			continue
		mean = data[i].mean()
		std = data[i].std()
		means[i] = mean # store for use in testing
		stds[i] = std # store for use in testing
		data.loc[:,i] -= mean
		if std!=0:
			data.loc[:,i] /= std 
	return data,means,stds
	

# this function takes input the raw input data and updates it by changing the symbols as follow:
# M = [ 1 , 0 , 0 ]
# F = [ 0 , 1  , 0 ]
# I = [ 0 , 0  , 1 ]
def preprocessing(data):
	gender = data[0]
	males = []
	females = []
	infants = []
	ones = []
	for i in gender:
		ones = ones + [1]
		if i=='M':
			males = males + [1]
			females = females + [0]
			infants = infants + [0]
		elif i=='F':
			males = males + [0]
			females = females + [1]
			infants = infants + [0]
		else:
			males = males + [0]
			females = females + [0]
			infants = infants + [1]
	
	# delete the existing symbols
	del data[0]
	# add the new columns corresponding to the symbols
	data[8] = males
	data[9] = females
	data[10] = infants
	data[0] = ones
	return data
	

# this function takes out fr% data from the input and makes it the test set
# the remaining rows become the train set
def getRandomData(data , fr ):
	train = data.sample(frac=fr)
	test = data.loc[~data.index.isin(train.index)]
	return train , test	

#  caller for linear regression
def run_linear_reg( fraction , lambda_):
	data = pd.read_csv("linregdata" , header=None) # read data from the file
	if len(data.columns)!=9:
		print ("Data configuration error")
		exit()
	train , test  = getRandomData(data , 0.8 )
	train , val  = getRandomData( train, fraction )
	age_Y = train[8]
	age_Y_t = test[8]
	del train[8]
	del test[8]
	
	# convert the symbols to corresponding indicator matrix values
	train = preprocessing(train)
	test = preprocessing(test)

	# standardize the inputs
	train , means , stds = getStandardizedTrainData(train)
	test = getStandardizedTestValData(test , means , stds )
	
	# convert from panda dataframe to numpy array for further processing
	train = train.values
	age_Y= age_Y.values
	age_Y = age_Y.reshape((len(age_Y),1))

	test = test.values
	age_Y_t = age_Y_t.values
	age_Y_t = age_Y_t.reshape((len(age_Y_t),1))
	
	# calculate the W matrix
	W = mylinridgereg(train , age_Y , lambda_ )
	acc_train = meansquarederr( mylinridgeregeval(train,W) , age_Y ) # train error
	acc_test = meansquarederr( mylinridgeregeval(test,W) , age_Y_t ) # test error
	return acc_train , acc_test

if __name__ =="__main__":
	pd.options.mode.chained_assignment = None
	lambda_ = [0.01 , 0.02 , 0.05, 0.1 , 0.2 , 0.5 , 1 , 1.5 , 2 , 2.5 ] # , 4 , 6 ,8 , 10 ]
	fractions = [0.1 , 0.3 , 0.5 , 0.7 , 0.9 , 0.97] # train set fractions
	print("Number of iterations = " + str(itr) )
	# run the linear regression model 100 times for all combinations of lambda and test set fraction
	# the output will be the list of averaged errors
	min_ = []
	min_i = []
	for fr in fractions:
		print("Running for Train Fraction = " + str(fr) ) 
		o_tr = []
		o_te = []
		for k in lambda_:
			tr_l = []
			te_l = []
			for i in range(10):
				tr , te = run_linear_reg(  fr , k )
				tr_l.append(tr)
				te_l.append(te)
			a = numpy.mean( numpy.array(tr_l) )
			o_tr.append( a ) 
			b = numpy.mean( numpy.array(te_l) )
			o_te.append( b )
		b = numpy.min( numpy.array(o_te))
		min_.append(b)
		b = numpy.argmin(numpy.array(o_te))
		min_i.append(lambda_[b])

		plt.plot(lambda_ , o_tr , 'b' , label = "Train error" )
		plt.plot( lambda_ , o_te , 'r' , label = "Test error")
		plt.title("Fraction = " + str(fr) )
		plt.legend(loc='upper left')
		plt.xlabel("Value of Lambda")
		plt.ylabel('Mean Squared Error')
		plt.savefig( "Fr:" + str(fr) + ".png" )
		plt.close()
		
	plt.plot( fractions , min_ , 'b' )
	plt.scatter( fractions , min_i )
	plt.plot( fractions , min_i , 'y' , label = "Value of lambda")
	plt.title("Red dot is the corresponding value of lambda" )
	plt.legend(loc='upper left')
	plt.xlabel("Value of Train set fraction")
	plt.ylabel('Minimum Mean Squared Error')
	plt.savefig( "Min_err" + ".png" )
	plt.close()

		
	for k in lambda_:
		print("Running for Lambda = " + str(k) ) 
		o_tr = []
		o_te = []
		min_ = []
		min_i = []
		for fr in fractions:
			tr_l = []
			te_l = []
			for i in range(10):
				tr , te = run_linear_reg(  fr , k )
				tr_l.append(tr)
				te_l.append(te)
			a = numpy.mean( numpy.array(tr_l) )
			o_tr.append( a ) 
			b = numpy.mean( numpy.array(te_l) )
			o_te.append( b )
			
		plt.plot(fractions , o_tr , 'b' , label = "Train error" )
		plt.plot( fractions , o_te , 'r' , label = "Test error")
		plt.title("Lambda = " + str(k) )
		plt.legend(loc='upper left')
		plt.xlabel("Value of Train set fraction")
		plt.ylabel('Mean Squared Error')
		plt.savefig( "L:" + str(k) + ".png" )
		plt.close()
		
		
