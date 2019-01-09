Prerna Garg
2016csb1050
CSL333 Assignment-3

1) Instructions to run the code
javac DeadlockDetect.java
java DeadlockDetect proc_data.csv

2) Input format 
Input is a csv file of the following format:
In a system having n processes and m resources the CSV file has n rows and 2*m columns. First m columns correspond to allocation data and next m columns correspond to requested data. The first row has additional m columns that contain the availability data.
Example CSV file:
0,2,1,0,2,1,2,0,1,0,6,4,1,3,2,3,2,1
1,1,2,1,0,0,3,2,1,2,5,0
2,0,0,0,2,0,0,1,0,0,1,0
1,0,0,2,0,2,0,3,0,0,2,1
1,0,1,0,0,2,1,0,2,0,0,2

5 Processes and 6 Resources
W = [ 1,3,2,3,2,1 ] 

P = [ [0,2,1,0,2,1] , 
		 [1,1,2,1,0,0] , 
		 [2,0,0,0,2,0] ,
		 [1,0,0,2,0,2] ,
		 [1,0,1,0,0,2] ]
		 
Q = [ [2,0,1,0,6,4] ,
		  [3,2,1,2,5,0] ,
		  [0,1,0,0,1,0] ,
		  [0,3,0,0,2,1] ,
		  [1,0,2,0,0,2] ]

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
Both issues are being detected in my code.

4) Sample Run:

0,2,1,0,2,1,2,0,1,0,6,4,1,3,2,3,2,1
1,1,2,1,0,0,3,2,1,2,5,0
2,0,0,0,2,0,0,1,0,0,1,0
1,0,0,2,0,2,0,3,0,0,2,1
1,0,1,0,0,2,1,0,2,0,0,2
Using input from test.csv
System state: Deadlocked. Processes: P1, P2. Resources: R5.

0,2,3,1,0,0,0,1,2,2,0,0
1,1,0,0,2,2,0,0
0,0,1,1,0,0,0,1
Using input from test2.csv
System state: Deadlocked. Processes: P1, P3. Resources: R4.

0,0,0,0,5,1,1,1,2,2,4,4
0,0,0,0,2,2,0,1
0,0,0,0,0,0,0,1
Using input from test3.csv
System state: Deadlocked. Processes: P1. Resources: R1.
Note: In this example no process is holding resources while some other process needs them. Rather P1 is requesting resources more than total available in the system irrespective of other processes in the system.

