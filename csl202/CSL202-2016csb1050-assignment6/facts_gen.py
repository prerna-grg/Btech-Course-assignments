import yaml
import time
import sys
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# the following function is used to generate prlog rules and facts for the machine_info.yaml data
def getPrologRules():
	f = open("facts_and_rules.pl" , "w") #open the file in write mode
	with open("./WDog/machine_info.yaml", 'r') as myfile:
		data = myfile.read().replace("\t","    ") # because yaml.load does not considers \t as valid indentation
		new_lines = "-"+"\n"
		lines = data.split("\n")
		lines = lines[:-1]
		empty_line = re.compile("^[\\s]*$")
		for i in lines:
			if re.search(empty_line, i ) != None:
				new_lines = new_lines + "-" + "\n\n"
			else:
				new_lines = new_lines + "\t" + i.rstrip() + "\n"
		
		data = new_lines.replace("\t","    ") # because yaml.load does not considers \t as valid indentation
		try:
			a = yaml.load(data) # load the data at once
		except yaml.YAMLError as exc:
			print(exc)


	my_machines = [] # list of machines in yaml file
	my_softwares = [] # list of software applications in yaml file
	my_OS = [] # list of operating systems in yaml file

	for entity in a:
		key = next(iter(entity))
		if "OS" in key:
		    my_OS.append(entity) # primary key is OS

		elif "Machine" in key:
		    my_machines.append(entity) # primary key is Machine     

		elif "SoftwareApp" in key:
		    my_softwares.append(entity) # primary key is Software app

	for i in my_OS:  # writing to prolog file in the form of a fact
		f.write("isOS(" + str(i['OS']['id']) + "," + i['OS']['name'] + "," + str(i['OS']['version']) + "," + str(i['OS']['arch']).split(" ")[0] + "," + str(i['OS']['limits']['max_open_files']) + "," + str(i['OS']['limits']['max_connections']) + "," + str(i['OS']['provides_libs']) + ")." + "\n") 
	
	for i in my_machines:  # writing to prolog file in the form of a fact
		temp = i['Machine']['RAM'].split(" ")
		temp[0] = float(temp[0])
		ram = temp[0]
		# converting RAM to a standard unit MB
		if( temp[1] == "KB" ):
			ram = temp[0]/1024
		elif( temp[1] == "GB" ):
			ram = temp[0]*1024
		elif( temp[1] == "B" ):
			ram = (temp[0]/1024)/1024
		
		temp = i['Machine']['disk'].split(" ")
		temp[0] = float(temp[0])
		disk = temp[0]
		# converting disk to a standard unit GB
		if( temp[1] == "MB" ):
			disk = temp[0]/1024
		elif( temp[1] == "KB" ):
			disk = (temp[0]/1024)/1024
		elif( temp[1] == "B" ):
			disk = ((temp[0]/1024)/1024)/1024
		elif( temp[1] == "TB" ):
			disk = temp[0]*1024
	
	
		f.write("isMachine(" + str(i['Machine']['id']) + "," + "'" + i['Machine']['type'] + "'" + "," + str(i['Machine']['OS']) + "," + str(ram) + "," + str(disk) + "," + str(i['Machine']['CPU']).split(" ")[0] + ")." + "\n")

	for i in my_softwares:  # writing to prolog file in the form of a fact
		temp = i['SoftwareApp']['requires_hardware']['min_RAM'].split(" ")
		temp[0] = float(temp[0])
		ram = temp[0]
		# converting RAM to a standard unit MB
		if( temp[1] == "KB" ):
			ram = temp[0]/1024
		elif( temp[1] == "GB" ):
			ram = temp[0]*1024
		elif( temp[1] == "B" ):
			ram = (temp[0]/1024)/1024
		
		# converting disk to a standard unit GB
		temp = i['SoftwareApp']['requires_hardware']['min_disk'].split(" ")
		temp[0] = float(temp[0])
		disk = temp[0]
		if( temp[1] == "MB" ):
			disk = temp[0]/1024
		elif( temp[1] == "KB" ):
			disk = (temp[0]/1024)/1024
		elif( temp[1] == "B" ):
			disk = ((temp[0]/1024)/1024)/1024
		elif( temp[1] == "TB" ):
			disk = temp[0]*1024
	
	
		f.write("isApp(" + str(i['SoftwareApp']['id']) + "," + "'" + i['SoftwareApp']['name'] + "'" + "," + str(ram) + "," + str(disk) + "," + str(i['SoftwareApp']['requires_hardware']['min_CPU'].split(" ")[0]) + "," + str(i['SoftwareApp']['requires_software']['OS']) + "," + str(i['SoftwareApp']['requires_software']['libs']) + ")." + "\n")
	
	
	# writing prolog rules for the query execution
	f.write("\nfound(X,[X|Tail]).\nfound(X,[_|Tail]):- found(X,Tail).\n\nsubs([], _).\nsubs([X|Tail], Y):- found(X, Y),subs(Tail, Y).\n\nfindMachine(X,L):-isApp(X,A,B,C,D,E,F),isMachine(L,M,N,O,P,Q),O>=B,P>=C,Q>=D,isOS(N,_,_,_,_,_,W),subset(F,W),write(" + "\"\\" + "nID: \"),write(L),write("  + "\"\\" + "nType: \"),write(M),write(" + "\"\\" + "nOS: \"),write(N),write("  + "\"\\" + "nRAM: \"),write(O),write("  + "\"" + " MB" + "\\" + "ndisk: \"),write(P),write(\"GB"  + "\\" + "nCPU: \"),write(Q),write(\" cores\"),write(" + "\"\\" + "n\")."+ "\n\ncheckAppMachine(X,Y,Y):-isApp(X,_,B,C,D,_,F),isMachine(Y,M,N,O,P,Q),O>=B,P>=C,Q>=D,isOS(N,_,_,_,_,_,W),subset(F,W).\n")
	


# Optional watchDog application to detect changes in yaml file and reload the prolog facts and rules, to achieve this functionality the current file facts_gen.py will keep running
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
    	getPrologRules() # reload when change is detected
        print "machine_info.yaml changed..Re-loading the prolog file!!" # notify the reload to the user 


if __name__ == "__main__":

	if len(sys.argv)==2:
		if sys.argv[1] == "-i":
			getPrologRules()
			event_handler = MyHandler()
			observer = Observer()
			observer.schedule(event_handler, path='./WDog', recursive=False)
			observer.start()

			try:
				while True:
					time.sleep(1)
			except KeyboardInterrupt:
				observer.stop()
			observer.join()
	else:
		getPrologRules() # load the rules and finish
