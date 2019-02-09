To run the code execute in the following structure:

I have used pickle library of python to store the trained models. The time taken for the codes to run (especially for decision forest) is quite longer. Therefore to use the pre-trained models for evaluation, execute:

python3 decision_tree.py data.txt expt_no 

Example: 
python3 decision_tree.py data.txt 2 

However If you require to retrain the entire model, execute:
python3 decision_tree.py data.txt expt_no -n
python3 decision_tree.py data.txt 2 -n
The -n flag will recreate the models

The version of python required to run this code is python 3.x
1000 instances have been selected from each train and test folder and stored into the file name "data.txt", with first 1000 being the training set and next 1000 being the test set. In case of pruning this test set is used as validation set.
6000 words have been selected from thre given 89000 words and stored in the file named selected-features-indices.txt , from where they are read every time the code is run.

The file gen_set.py is used to select random 1000 instances from the dataset. In case you want to renew the instances execute:
python3 gen_set.py
