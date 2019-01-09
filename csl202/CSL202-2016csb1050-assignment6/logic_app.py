import subprocess
import sys
from facts_gen import getPrologRules

if len(sys.argv)==2:
	if sys.argv[1] == "-i":
		getPrologRules()
		print ("The prolog facts and rules have been successfully reloaded")
			
# get user input to find which query is desired
print ("Enter 1 to list all the machines where a given application can be executed.")
print ("Enter 2 to find whether a given machine can execute a given application or not.")
query = input()

# query execution
if query == 1:
	print("Enter App ID: ") # software application ID
	appID = input() # user input
	# invoke swipl and get the output
	p = subprocess.Popen("swipl -q -g 'style_check(-singleton),[facts_and_rules],findall(Y,(findMachine(" + str(appID) + ",Y)), L),halt'", stdout=subprocess.PIPE, shell=True) # retreives all the machines data who can support the application
	(output, err) = p.communicate()
	# return empty string if no machine found
	if output == "":
		print ("\nSorry.There are no machines to run this application")
	else:
		print(output)
		print ("\nAbove listed are the machines where app will run.")

elif query == 2:
	print("Enter App ID: ") # software application ID
	appID = input()
	print("Enter Machine ID: ") # machine ID
	mID = input()
	# invoke swipl and get the output
	p = subprocess.Popen("swipl -q -g 'style_check(-singleton),[facts_and_rules],findall(Y,(checkAppMachine(" + str(appID) + "," + str(mID) + ",Y)), L),write(L),halt'", stdout=subprocess.PIPE, shell=True) 
	# return a string of empty list symbol if not supported, otherwise returns the same Machine ID in the list
	(output, err) = p.communicate()
	if output == "[]":
		print ("\nSorry.The application cannot run on this machine.")
	else:
		print ("\nYes.The application will run on this machine.")
	
else:
	print("Invalid Query") # anything except 1 or 2
