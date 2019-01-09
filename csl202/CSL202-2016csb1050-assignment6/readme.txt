Prerna Garg
2016csb1050
CSL202-Assignment 6


1. What does this program do

This program takes input a yaml file and creates suitable prologue facts to describe the information of OS, Machines and Software applications on which some queries can be executed. Any prolog fact describes one of the above mentioned things and is named isOS(), isMachine() , isSoftwareApp()
Following are the queries that can be executed:
1) get the list of all machines on which a specific application can be executed
2) check whether an application with given application ID can be run on a machine with given machine ID or not

If any changes have been made to the yaml file, there are two ways to reload thr prolog facts.
1) watchDog check in facts_gen.py -- 
to enable this check run the code with -i option, it will keep a check on mahcine_info.yaml file for any changes and will reload at every keyboard interrupt.
2) User input in logic_app.py --
Watchdog doesnot detect changes made when facts_gen.py is not running, and otherwise it has to run indefinitely to detect the changed and reload, to avoid this you can simply use the -i option while running logic_app.py to reload the prolog facts/queries

2. A description of how this program works (i.e. its logic)

This program has the following .py file :

facts_gen.py : this file reads data in a well defined format from the yaml file and writes prologue logic to facts_and_rules.pl. For duplicate keys from yaml file I have changed the format as follows:
-
	OS:
		ID:

-
	OS:
		ID:

This enables normal yaml.load to read duplicate keys without overwriting the data.
The code does not expect the hyphens and extra indentation to be present beforehand. They will added by me explicitly through a function.


logic_app.py : Both the queries are handled by this file. User input will be taken as and when needed.

3. How to compile and run this program

-- without check
python facts_gen.py

-- with check
python facts_gen.py -i

-- without check
python logic_app.py

-- with check
python logic_app.py -i

The machine info filename is machine_info.yaml and it is to be kept in a folder named WDog for watchdog usage.
