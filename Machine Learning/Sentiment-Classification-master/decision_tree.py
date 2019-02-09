from operator import itemgetter
from itertools import islice
import sys
import random
import math
import copy
import pickle
import os

terminal_nodes=0 # global variable for number of leaves
get_count = {} # dictionary that keeps count of which index was used how many times
global_accuracy = 0 # needed while pruning
prune_node = None # needed while pruning

# Node class for the tree object
class Node:

	def count_terminal_nodes(self):
		global terminal_nodes
		if self.left or self.right:
			if self.left:
				self.left.count_terminal_nodes()
			if self.right:
				self.right.count_terminal_nodes()
		else:
			terminal_nodes += 1 # this means current self is a leaf
			
	def getIndexUseCount(self):
		if not self :
			return
		if self.index==-1:
			return
		if self.index in get_count:
			get_count[self.index]+=1
		else:
			get_count[self.index] = 1
		if self.left:
			self.left.getIndexUseCount()
		if self.right:
			self.right.getIndexUseCount()

	def printTree(self):
		print ( str(self.index) + " " + str(len(self.lists)) )
		if self.left:
			self.left.printTree()
		if self.right:
			self.right.printTree()

	def __init__(self, index , lists):
		self.left = None # left child
		self.right = None # right child
		self.lists = lists # feature vectors arriving at this particular node
		self.leaf = 0 # label of the leaf (initially unlabelled)
		self.index = index # index where the split occurs
		self.level = -1 


# gets the top most words in decreasing order of sentiments ( pos_words for positive , neg_words for negative )
def createVocab(pos_words_req , neg_words_req):

	words_file = open("../project1/aclImdb/imdbEr.txt" , "r")
	w1 = words_file.readlines() # vocabulary
	num_words = 0 # number of words in the file
	for line in w1:
		num_words+=1
	
	words_val = [[0 for x in range(2)] for y in range(num_words)]
	# store the index apriori
	for i in range(num_words):
		words_val[i][1] = i
	with open("../project1/aclImdb/imdbEr.txt", "r") as input_data:
		num = 0
		for each_line in input_data:
			try:
				words_val[num][0] = float(each_line.strip())
				num += 1
			except ValueError as e:
				print('Warning: Unable to parse %s: %s' % (each_line, e),file=sys.stderr) # cannot convert string to float

	# sort the words according to the value of their sentiment
	words_val = sorted(words_val,key=itemgetter(0))
	my_vocab = []
	
	# get the top most words for your dictionary
	for i in range(neg_words_req):
		my_vocab.append(words_val[i][1])
		
	for i in range(pos_words_req):
		my_vocab.append(words_val[num_words-i-1][1])
	
	# writing the output
	my_words = open("selected-features-indices.txt" , "w")
	for vocab in my_vocab:
		my_words.write(str(vocab)+ "\n")
	return


def getVocab():
	my_dict = dict()
	with open("selected-features-indices.txt", "r") as input_data:
		for each_line in input_data:
			my_dict[int(each_line)] = 1
	return my_dict
	

# calculates the feature vectors for all the reviews based on words in the dictionary and returns a list of dictionaries	
def getFeatureVector(my_dict , file_name  ):
	rev_file = open( file_name , "r")
	feature_vectors = []
	# read the line and get the label
	for line in rev_file:
		temp_f = dict()
		lines = line.split(" ")
		temp_f["label"] = 0
		if int(lines[0])>=7:
			temp_f["label"] = 1
		if int(lines[0])<=4:
			temp_f["label"] = -1
		
		lines = lines[1:]
		# get all the words and their frequencies present in the review
		for i in lines:
			is_to = i.split(":")
			# check if it exists in the mini dictionary we have created
			if int(is_to[0]) in my_dict.keys():
				temp_f[int(is_to[0])] = 1
		feature_vectors.append(temp_f)
	return feature_vectors


# assigns label for leaf nodes i.e. maximum occurring label among the elements of argument lists
def getMaxCountLabel(lists):
	p_count = 0 # number of positive labels
	n_count = 0 # number of negative labels
	for inst in lists:
		if inst["label"] == 1:
			p_count += 1
		if inst["label"] == -1:
			n_count += 1
	if p_count>n_count:
		return 1
	else:
		return -1


# adds random noise to the train data set
def add_noise(percent , feature_vector):
	len_l = len(feature_vector)
	len_c = int((len_l * percent) / 100)
	to_change = random.sample(range(0, len_l), len_c)
	for i in to_change:
		if feature_vector[i]["label"]==1:
			feature_vector[i]["label"] = 0
		else:
			feature_vector[i]["label"] = 1
	return feature_vector	
	
	
# traverses the tree with starting point "root" to find label for the feature vector f_v
def get_label( f_v , root ):
	if root.leaf != 0:
		return root.leaf
	else:
		if root.index in f_v.keys():
			return get_label( f_v , root.left )
		else:
			return get_label( f_v , root.right )
	

# function to calculate entropy of labels of a set of instances
def entropy(input_inst):
	p_count = 0 # number of positive labels
	n_count = 0 # number of negative labels
	for inst in input_inst:
		if inst["label"] == 1:
			p_count += 1
		if inst["label"] == -1:
			n_count += 1
	if p_count == 0 or n_count==0:
		return 0
	sums = p_count + n_count
	# find respective probabilities
	p_count /= sums 
	n_count /= sums
	return (-1*p_count*(math.log(p_count,2))) + (-1*n_count*(math.log(n_count,2)))


# traverses the root for all the features to find if the tree correctly labels them or not and returns the accuracy
def get_accuracy( root , features ):
	c_=0
	for i in features:
		label = get_label( i , root )
		if label == i["label"]:
			c_ += 1
	test_accuracy = 100*c_/(len(features))
	return test_accuracy


# Function for Post Pruning
# Parameters:
	# root always points to the top most node of the tree
	# node points to the one for which we are considering pruning in this particular call
	# validation set is a small data set used to decide whether to prune or not
def post_prune( root , node , validation_set ):
	global prune_node 
	global global_accuracy
	if node==None:
		return
	if node.left == None or node.right == None :
		return
	temp_l = copy.deepcopy(node.left)
	temp_r = copy.deepcopy(node.right)
	node.left = None
	node.right = None
	node.leaf = getMaxCountLabel(node.lists)
	new_accr = get_accuracy(root,validation_set)
	# restore the state of the node
	node.left = copy.deepcopy(temp_l)
	node.right = copy.deepcopy(temp_r)
	node.leaf = 0
	# if accuracy is greater than that found on removing any other node then update the stored data
	if new_accr >= global_accuracy:
		global_accuracy = new_accr
		prune_node = node
	
	# recursive call for the children
	if node.left:
		post_prune(root , node.left , validation_set )
	if node.right:
		post_prune(root , node.right , validation_set )
	
	
# create the tree with the given feature vectors/dictionary/stopping criteria
def makeTree( en_p , feature_vector , my_dict , stopping_criteria , num , limit2 , limit ):
	if len(feature_vector)==0:
		return None
	if (stopping_criteria=="inst" and len(feature_vector)<num ) or  (stopping_criteria=="depth" and num>limit2) :
		root = Node(-1,[])
		root.left = None
		root.right = None
		root.lists = feature_vector
		root.leaf = getMaxCountLabel(feature_vector)
		return root
			
	root = Node(-1,[])
	root.lists = feature_vector
	max_info_gain = -1
	max_IG_key = -1
	left = []
	right = []
	en_1 = 0 
	en_2 = 0
	# find the index where to split by finding the node that causes maximum information gain
	for key in my_dict.keys():
		list1 = [] 
		list2 = []
		for vec in root.lists:
			if key in vec.keys():
				list1.append(vec)
			else:
				list2.append(vec)

		en1 = entropy(list1)
		en2 = entropy(list2)
		
		Info_gain = en_p - float( len(list1)/len(feature_vector))*en1  - float( len(list2)/len(feature_vector))*en2 
		if Info_gain>max_info_gain:
			max_info_gain = Info_gain
			max_IG_key = key
			left = list1
			right = list2
			en_1 = en1
			en_2 = en2
	
	# if it less than some particular limit do not split , create a leaf ,  label it and return
	if max_info_gain<=limit :
		root.left = None
		root.right = None
		root.lists = feature_vector
		root.leaf = getMaxCountLabel(feature_vector)
		return root
	
	root.index = max_IG_key
	# in the subsequent dictionary do not pass the node that already caused the splitting
	my_new_dict = {}

	for key2 in my_dict.keys():
		if key2==max_IG_key:
			continue
		else:
			my_new_dict[key2] = 1

	# recursively call for both the children
	if en_1>0:
		root.left = makeTree ( en_1 , left , my_new_dict , stopping_criteria ,num+1, limit2 , limit)
	elif len(left)>0:
		root.left = Node(-1,left)
		root.left.leaf = getMaxCountLabel(left)
	else:
		root.left = None

	if en_2>0:
		root.right = makeTree ( en_2 , right , my_new_dict , stopping_criteria , num+1, limit2 , limit )
	elif len(right)>0:
		root.right = Node(-1,right)
		root.right.leaf = getMaxCountLabel(right)
	else:
		root.right = None
	
	return root


if __name__ =="__main__":
	
	if len (sys.argv)<3 :
		print ( "Usage For Pre-trained Model: python decision_tree.py data.txt expt_no")
		print ( "Usage To Train a new Model: python decision_tree.py data.txt expt_no -n")
		exit()
		
	# number of words in the dictionary
	words_req = 6000
	#createVocab(3000,3000)
	_dict = getVocab()
	# read the data fromt the file
	if not os.path.exists( sys.argv[1]):
		os.system("gen_set.py")
	features = getFeatureVector(_dict ,  sys.argv[1]) # get the feature vectors
	# get the train and test sets
	len_f = int(len(features)/2)
	train_features = features[:len_f]
	test_features = features[len_f:]
	# print the necessary attributes
	print ( "No. of words in dictionary = " + str(words_req))
	print ( "No. of instances in Training Set = " + str(len(train_features)))
	print ( "No. of instances in Test Set = " + str(len(test_features)))
	print("\nStarting with Tree formation")
	root = None
	train_accuracy = 0
	test_accuracy = 0
	# 1. make a decision tree 
	if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("root_model.pkl"):
		root = makeTree( entropy(train_features), train_features , _dict , "" , 0 , 0 ,0  ) # make the decision tree
		train_accuracy = get_accuracy( root , train_features )
		test_accuracy = get_accuracy( root , test_features )
		print("\n")
		print ( "Train Accuarcy: " + str(train_accuracy))
		print ( "Test Accuarcy: " + str(test_accuracy))
		terminal_nodes = 0
		root.count_terminal_nodes()
		print ( "Number of terminal Nodes: " + str(terminal_nodes))
		save_file = open("root_model.pkl","wb") # save the model
		pickle.dump(root,save_file)
		save_file.close()
	else:
		save_file = open("root_model.pkl","rb") # load the existing model
		root = pickle.load(save_file)
		
	# 2. Print the nodes used for splitting ( top 10 )
	get_count = {}
	root.getIndexUseCount()
	list_count = [ [k,v] for k, v in get_count.items() ]
	list_count = sorted(list_count,key=itemgetter(1))
	print ( "\nTop 10 elements used for splitting" )
	for h in range(10):
		print ( str(list_count[len(list_count)-h-1][0] + 1) + " : " +  str( list_count[len(list_count)-h-1][1] ) )
	
	# Experiment No. 2
	if sys.argv[2] == "2":
		print ( "Early Stopping")
		limit_depth = [5,15,17,18,20,25]
		limit_inst = [5,10,15,20,25,30]
		limit_ig = [ 0.001 , 0.002 , 0.003 , 0.004 ]
		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("early_stop_d.pkl"):
			early_stop = []
			for i in limit_depth:
				tree = makeTree( entropy(train_features), train_features , _dict , "depth" , 0 , i  , 0)
				early_stop.append(tree)
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for maximum depth = " + str(i) )
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			save_file = open("early_stop_d.pkl","wb")
			pickle.dump(early_stop,save_file)
			save_file.close()
			
		else:
			save_file = open("early_stop_d.pkl","rb")
			early_stop = pickle.load(save_file)
			i=0
			for tree in early_stop:
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for maximum depth = " + str(limit_depth[i]) )
				i+=1
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
	
		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("early_stop_n.pkl"):
			early_stop = []
			for i in limit_inst:
				tree = makeTree( entropy(train_features), train_features , _dict , "inst" , i , 0 , 0)
				early_stop.append(tree)
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for minimum number of instances while splitting = " + str(i) )
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			save_file = open("early_stop_n.pkl","wb")
			pickle.dump(early_stop,save_file)
			save_file.close()
			
		else:
			save_file = open("early_stop_n.pkl","rb")
			early_stop = pickle.load(save_file)
			i = 0
			for tree in early_stop:
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for minimum number of instances while splitting = " + str(limit_inst[i]) )
				i+=1
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))

		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("early_stop_ig.pkl"):
			early_stop = []
			for i in limit_ig:
				tree = makeTree( entropy(train_features), train_features , _dict , "infog" , 0 , 0 , i )
				early_stop.append(tree)
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for minimum information gain = " + str(i) )
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			save_file = open("early_stop_ig.pkl","wb")
			pickle.dump(early_stop,save_file)
			save_file.close()
		else:
			save_file = open("early_stop_ig.pkl","rb")
			early_stop = pickle.load(save_file)
			i=0
			for tree in early_stop:
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print("\n")
				print ( "Decision Tree Built for minimum information gain = " + str(limit_ig[i]) )
				i+=1
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			
	# Experiment No. 3
	elif sys.argv[2] == "3":
		print ( "Random Noise Analysis")
		noise = [0.5,1,5,10]
		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("noisy_models.pkl"):
			noisy_models = []
			for perc in noise:
				train_features_n = add_noise( perc , train_features )
				print ( "\nAdded " + str(perc) + "% random noise" )
				tree = makeTree( entropy(train_features), train_features , _dict , "" , 0 ,0 , 0)
				noisy_models.append(tree)
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print ( "Decision Tree Built with noise = " + str(perc) + " %" )
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			save_file = open("noisy_models.pkl","wb")
			pickle.dump(noisy_models,save_file)
			save_file.close()
		else:
			save_file = open("noisy_models.pkl","rb")
			noisy_models = pickle.load(save_file)
			g = 0
			for perc in noise:
				print ( "\nAdded " + str(perc) + "% random noise" )
				tree = noisy_models[g]
				g+=1
				train_accuracy = get_accuracy( tree , train_features )
				test_accuracy = get_accuracy( tree , test_features )
				print ( "Decision Tree Built with noise = " + str(perc) + " %" )
				print ( "Train Accuarcy: " + str(train_accuracy))
				print ( "Test Accuarcy: " + str(test_accuracy))
				#global terminal_nodes 
				terminal_nodes = 0
				tree.count_terminal_nodes()
				print ( "Number of terminal Nodes: " + str(terminal_nodes))
			
	# Experiment No. 4
	elif sys.argv[2] == "4":
		print ( "\nEffect of Pruning the tree . . .")
		global_accuracy = test_accuracy
		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("pruned_tree.pkl") or not os.path.exists("pruned_data.pkl") :
			accuracies = []
			while True:
				prune_node = root
				post_prune( root , root , test_features)
				if global_accuracy>test_accuracy:
					prune_node.leaf = getMaxCountLabel(prune_node.lists)
					prune_node.left = None
					prune_node.right = None
					print ( str(len(accuracies)+1) + " : " + str(global_accuracy))
					accuracies.append(global_accuracy)
					test_accuracy = global_accuracy
				else:
					break
			save_file = open("pruned_tree.pkl","wb")
			pickle.dump(root,save_file)
			save_file.close()
			save_file = open("pruned_data.pkl","wb")
			pickle.dump(accuracies,save_file)
			save_file.close()
		else:
			save_file = open("pruned_tree.pkl","rb")
			root = pickle.load(save_file)
			save_file = open("pruned_data.pkl","rb")
			accuracies = pickle.load(save_file)
			for acc in range(len(accuracies)):
				print ( str(acc+1) + " : " + str(accuracies[acc]))
			
		print( "\nResult after Pruning the tree")
		train_accuracy = get_accuracy( root , train_features )
		test_accuracy = get_accuracy( root , test_features )
		print ( "Decision Tree Built" )
		print ( "Train Accuarcy: " + str(train_accuracy))
		print ( "Test Accuarcy: " + str(test_accuracy))
		#global terminal_nodes 
		terminal_nodes = 0
		root.count_terminal_nodes()
		print ( "Number of terminal Nodes: " + str(terminal_nodes))
	
	# Experiment No. 5	
	elif sys.argv[2] == "5":
		print ( "Creating a Decision Forest")
		number_of_trees = [5,10,15,20]
		if (len(sys.argv)==4 and sys.argv[3] == "-n") or not os.path.exists("forests.pkl"):
			list_of_forests = []
			n = 4000
			print ( "Number of words selected at random = " + str(n))
			for n_t in number_of_trees:
				forest = []
				list_dict = [ [k,v] for k, v in _dict.items() ]
				for itr in range(n_t):
					new_dict = {}
					random.shuffle(list_dict)
					for i in range(n):
						new_dict[list_dict[i][0]] = list_dict[i][1]
					root = makeTree( entropy(train_features), train_features , new_dict , "" , 0 , 0 , 0)
					forest.append(root)
				list_of_forests.append(forest)
			save_file = open("forests.pkl","wb")
			pickle.dump(list_of_forests,save_file)
			save_file.close()
		else:
			save_file = open("forests.pkl","rb")
			list_of_forests = pickle.load(save_file)
		
		print ( "Number of Trees -- Train Accuracy -- Test Accuracy")
		t1 = []
		t2 = []
		for forest in list_of_forests:
			c_ = 0
			for i in train_features:
				p_c = 0
				n_c = 0
				for tree in forest:
					label = get_label( i , tree )
					if label==-1:
						n_c += 1
					else:
						p_c += 1
				if p_c >= n_c:
					label = 1
				else:
					label -1
				if label == i["label"]:
					c_ += 1
			t1.append((100*c_)/(len(test_features)))

			c_ = 0
			for i in test_features:
				p_c = 0
				n_c = 0
				for tree in forest:
					label = get_label( i , tree )
					if label==-1:
						n_c += 1
					else:
						p_c += 1
				if p_c >= n_c:
					label = 1
				else:
					label -1
				if label == i["label"]:
					c_ += 1
			t2.append((100*c_)/(len(test_features)))
		
		for i in range(len(number_of_trees)):
			print ( str(number_of_trees[i]) + " " + str(t1[i]) + " " + str(t2[i]))
