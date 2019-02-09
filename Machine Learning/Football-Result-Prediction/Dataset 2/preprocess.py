import pandas as pd
import numpy as np
 #!/usr/bin/env python -W ignore::DeprecationWarning
import pandas as pd
from sklearn.decomposition import PCA
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

def preprocess_features(X):
    # Preprocesses the football data and converts catagorical variables into dummy variables.
    # Initialize new output DataFrame
    output = pd.DataFrame(index = X.index)
    # Investigate each feature column for the data
    for col, col_data in X.iteritems():
        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix = col)
        # Collect the revised columns
        output = output.join(col_data)
    return output


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


def downSample(data):
	df_minority = data[ data.FTR == 'H' ]
	df_majority = data[ data.FTR == 'NH' ]
	# Downsample majority class
	df_majority = resample(df_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=len(df_minority),     # to match minority class
                                 random_state=122)
	data = pd.concat([df_majority, df_minority])
	return data


def preprocess():
	pd.options.mode.chained_assignment = None
	data = pd.read_csv('dataset2.csv')
	data = downSample(data)
	y_all = []
	
	for i in data.index:
		if data['FTR'][i] == 'H' :
			y_all.append(1)
		else:
			y_all.append(-1)
	y_all = np.array( y_all )
	
	X_all = data.drop(['FTR'],1)
	X_all = X_all.drop(['FTHG'],1)
	X_all = X_all.drop(['FTAG'],1)
	X_all = X_all.drop(['Date'],1)
	
	n_matches = X_all.shape[0]
	n_homewins = len(y_all[y_all == 1])
	win_rate = (float(n_homewins) / (n_matches)) * 100
	print( "Total number of matches: {}".format(n_matches))
	print( "Number of matches won by home team: {}".format(n_homewins))
	print( "Win rate of home team: {:.2f}%".format(win_rate))
	
	cols = [['HTGD','ATGD','HTP','ATP','DiffLP']]
	for col in cols:
		X_all[col] = scale(X_all[col])
	X_all.HM1 = X_all.HM1.astype('str')
	X_all.HM2 = X_all.HM2.astype('str')
	X_all.HM3 = X_all.HM3.astype('str')
	X_all.AM1 = X_all.AM1.astype('str')
	X_all.AM2 = X_all.AM2.astype('str')
	X_all.AM3 = X_all.AM3.astype('str')
	print( "Initial feature columns ({} total features)".format(len(X_all.columns) ))
	X_all = preprocess_features(X_all)
	#print(list(X_all.columns.values))
	print( "Processed feature columns ({} total features)\n".format(len(X_all.columns) ))
	X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, 
                                                    test_size = .3,
                                                    random_state = 200,
                                                    stratify = y_all)
	
	X_train = X_train.values
	X_test = X_test.values
	y_train = y_train.astype(np.float64)
	X_train,means,stds = getStandardizedTrainData(X_train)
	X_test = getStandardizedTestData(X_test , means , stds)
	y_train = y_train.reshape ( (len(y_train) ,1) )
	y_test = y_test.reshape ( (len(y_test) ,1) )
	return 	X_train, y_train , X_test, y_test
