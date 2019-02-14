# Deadlock-Detector

Java program to detect deadlock state given the current processes in a csv file

Prerna Garg

2016csb1050

CSL333 Assignment-3

1) Instructions to run the code

javac DeadlockDetect.java

java DeadlockDetect proc_data.csv

2) Input format 

Input is a csv file of the following format:

In a system having n processes and m resources the CSV file has n rows and 2*m columns. First m columns correspond to allocation data and next m columns correspond to requested data. The first row has additional m columns that contain the availability data.

3) Algorithm Explanation

We have the list of processes and resources at time t.

a) Let vector W denote the number of instances of all resources available in the system. 

b) P be a matrix where Pij = number of instances of resource j allotted to process i

c) Q be a matrix where Qij = number of instances of resource j requested by process i

d) Scan the processes. If Pi requests for Qi resources that is less than W then Pi will finish without going into deadlock. Therefore add Pi's values to W and mark the process to be done. However if Pi requesting for Qi resources is greater than available W then do not mark it and move to the next process to check if other processes will free resources. Once all the processes are scanned we will revisit the unmarked processes with updated W to check if they can be finished. We do this until our W keeps updating. Once W experiences no change on entire scan through P , we stop the algorithm. 

e) Now if any process is unmarked it is in deadlock. The responsible resources can be found by comparison with W.

Note:

A process may be in deadlock for 2 reasons:

Some other process is holding instances of resources needed by this process.

Or

This process is requesting more resources than total available in the system.
