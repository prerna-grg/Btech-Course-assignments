import pandas as pd
import numpy as np
 #!/usr/bin/env python -W ignore::DeprecationWarning
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.decomposition import PCA

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
	df_majority = data[ data['home_score'] - data['away_score'] >= 0 ]
	df_minority = data[ data['home_score'] - data['away_score'] < 0 ]
	# Downsample majority class
	df_majority = resample(df_majority, 
                                 replace=False,    # sample without replacement
                                 n_samples=len(df_minority),     # to match minority class
                                 random_state=122)
	data = pd.concat([df_majority, df_minority])
	return data


def preprocess():
	pd.options.mode.chained_assignment = None
	data = pd.read_csv('results.csv')
	data = downSample(data)
	X_all = data.drop(['home_score'],1)
	X_all = X_all.drop(['away_score'],1)
	X_all = X_all.drop(['date'],1)
	y_all = [] 
	for l in data.index:
		if data['home_score'][l] - data['away_score'][l] >= 0:
			y_all.append(1)
		else:
			y_all.append(-1)
	
	y_all = np.array( y_all )
	n_homewins = len( y_all[y_all == 1 ]) 
	n_matches = X_all.shape[0]
	win_rate = (float(n_homewins) / (n_matches)) * 100
	n_features = X_all.shape[1] - 1
	print( "Total number of matches: {}".format(n_matches))
	print( "Number of matches won by home team: {}".format(n_homewins))
	print( "Win rate of home team: {:.2f}%".format(win_rate))
	print( "Inbuilt feature columns ({} total features):\n".format(len(X_all.columns) ))
	X_all = preprocess_features(X_all)
	print( "Processed feature columns ({} total features):\n".format(len(X_all.columns) ))
	X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, 
                                                    test_size = .4,
                                                    random_state = 2,
                                                    stratify = y_all)
	
	X_train = X_train.values
	X_test = X_test.values
	y_train = y_train.astype(np.float64)
	
	X_train,means,stds = getStandardizedTrainData(X_train)
	X_test = getStandardizedTestData(X_test , means , stds)
	
	y_train = y_train.reshape ( (len(y_train) ,1) )
	y_test = y_test.reshape ( (len(y_test) ,1) )
	
	# To use PCA uncomment this block
	"""
	t = 500
	pca = PCA(n_components = t)
	X_train = pca.fit_transform(X_train,y_train)
	X_test = pca.transform(X_test)
	print( "Processed feature columns after PCA ({} total features):\n".format(len(X_train[0]) ))
	"""
	
	return 	X_train, y_train , X_test, y_test
