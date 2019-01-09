from bs4 import BeautifulSoup
import sys
import unicodedata

# to get line numbers from the file read it line by line and find links
def file_read(filename):
	f = open(filename , "r")
	my_links = {} #dictionary that will store all the deatils of the hyperlinks
	line_no = 1 # line number count
	link_id = 0 # id given specific to a hyperlink, useful while remove operations are carried out
	for line in f:
		soup = BeautifulSoup(line, 'html.parser') # find links in this line
		for link in soup.find_all('a' , href = True):
			link_id = link_id + 1 # increment the line id
			href = link.get('href') # extract it's href attribute
			data = link.text # extract it's text field
			# if already exists then append the data to existing href key else create a new key-value pair
			if href in my_links:
				my_links[href][0].append(data) # text in link
				my_links[href][1].append(line_no) # line number of link
				my_links[href][2].append(link) # link
				my_links[href][3].append(link_id) # link ID
				# store the text, line number, unique link ID, and href as a tuple in the dictionary with href as key
			else :
				my_links[href] =  [ [data] , [line_no] , [link] , [link_id] ]
				
		line_no = line_no + 1 # increment the line number
	return my_links
	

# this function counts the number of duplicates in the dictionary and returns the calcualted value
# Input is a dictionary containing href attribute as keys and link metadata and data as a value in the form of lists that define how many times the link has occurred
def num_dups(my_links):
	duplicates = 0 # initialisation
	for key in my_links:
		if len(my_links[key][3]) > 1:
			duplicates = duplicates + len(my_links[key][3])
	return duplicates
		

# This function is used to print the duplicate elements.. all duplicate elements of a particular link are printed together in order to picture a clear view, it also stores the serial numbers in which the links are displayed on the console and stores them along with existng data in a new dictionary
def print_dups(my_links):
	dup_links = {}
	serial_no = 1
	for key in my_links:
		if len(my_links[key][1]) > 1:
			dup_links[key] = ( my_links[key][0] , my_links[key][1] , my_links[key][2] , my_links[key][3] , [] )
			for j in range(len(my_links[key][1])):
				print ( str(serial_no) + ". " + key + " \"" + my_links[key][0][j] + "\"" + " at line " + str(my_links[key][1][j]) )
				dup_links[key][4].append(serial_no)
				serial_no = serial_no + 1
	
	return dup_links	
			

# This function ask the user for removal options that include "Removing None" , "Removing all except first occurrence" , "Remove all accept the user entered serial numbers"
def rem_dups( filename, dup_links):
	
	with open(filename) as fp:
	    soup = BeautifulSoup(fp,'html.parser')

	#soup = BeautifulSoup( filename , 'html.parser')
	print("\nSelect hyperlinks that you want to keep.\nEnter A to keep all, OR\nEnter F to keep the first one in a set of duplicates, OR\nEnter the serial numbers (separated by commas) of the links to keep.")
	
	order = input("Your selection: ")
	output_num = 0 # Number of links removed
	# user input for removal choice
	if order=='A':
		output_num = 0
	
	elif order=='F':
		temp_href = [] # list of those links whose first occurrence has been retained .. it helps to find out whether to remove the coming one or not
		for to_rem in soup.find_all('a'):
			href = to_rem.get('href')
			if href not in temp_href:
				temp_href.append(href)
			else:
				to_rem.decompose()
				output_num = output_num + 1
			 
	else:
		keep = order.split(',') # third choice i.e. retain the user input serial numbers
		for some in keep:
			if some.isdigit() == False:
				print("Invalid Inputs")
				return
			
		link_id_to_rem = []
		
		keep = list(map(int, keep))
		# collect the IDs to be removed
		for t in dup_links:
			for s in range(len(dup_links[t][4])):
				d = dup_links[t][4][s]
				if d not in keep:
					link_id_to_rem.append(dup_links[t][3][s])
		
		temp_link_id = 0
		# remove the collected IDs
		for to_rem in soup.find_all('a'):
			temp_link_id = temp_link_id + 1
			if temp_link_id in link_id_to_rem:
				to_rem.decompose()
				output_num = output_num + 1
	
	# write the output in a file in the directory from where the code has been executed
	out_file_name = "./" + filename + ".dedup"
	with open( out_file_name , "w") as file:
	    file.write(str(soup))
	    
	print ("\nRemoved " + str(output_num) + " hyperlinks. Output file written to " + out_file_name )

#read input
filename = sys.argv[1]
# get file numbers
my_links = file_read(filename)
# get number of duplicates
print("Found " + str(num_dups(my_links)) + " duplicates:")
# print duplicates
dup_links = print_dups(my_links)
# remove as user says
rem_dups(filename,dup_links)

