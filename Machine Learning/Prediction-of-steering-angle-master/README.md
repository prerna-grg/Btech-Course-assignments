# Prediction-of-steering-angle
Using Neural networks to predict the steering angle for a given road image

Before running the code please make sure this file is in the same directory where the steering folder exists.

Requirements to run the code:

1) Python3

2) opencv2

3) scipy , numpy , matplotlib

4) Pandas , pickle

Instrcutions to run the code:

python3 model.py


Outputs:

One graph and 3 pickle files are generated for each combination of parameters.

a) one for Neural network model

b) two for training and test accuracies used to create the graphs

Outputs are named using the following convention

(number of iterations)_(alpha)_(mini_batch_size)_(0/1 indicating whether dropout exists)

Example:

a) 1000_0.001_64_0.pkl (Neural Network model Name)

b) 1000_0.001_64_0_train.pkl (Train accuracies data)

c) 1000_0.001_64_0_test.pkl (Test accuracies data )

d) 1000_0.001_64_0.png (Graph)
