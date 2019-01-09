Submitter name: Prerna Garg
Roll No.: 2016CSB1050
Course: CSL333

=================================

1. What does this program do
This program is an implementation of 3 disk scheduling algorithms i.e. 
a) SSTF
b) C-SCAN
c) C-LOOK
The program generates a random disk cylinder request array and outputs the read-write head movement on the disk for the above 3 algorithms.

=================================

2. A description of how this program works (i.e. its logic)
There are 3 functions in the program that take input Requests Array and head
a) _SSTF_ : For a given head, the unserviced request with minimum distance from the head is found out and the corresponding distance is added to the total. This process is repeated till all the requests have been serviced.
b) _CSCAN_ : For a given head first the disk pointer goes to the rightmost end and services all requests coming in the way. Next if any request is left that was initially on the left side of the header it comes all the way back to the beginning without servicing anything and then goes right again to service the remaining.
c) _CLOOK_ : This is similar to C-SCAN with one difference that instead of going to the beginning and end of disk the pointer to goes to farthest and closest accessed thus saving some futile work.

For C-SCAN and C-LOOK there were some variations in the materials I referred on the internet in terms of whether to always go left/right/neares end first and if moving from the last sector to the first can be done directly without any movement or should be done by backward traverse and moving a distance equal to the total number of cylinders.

NOTE: My code is built on the rule that pointer always go to the right end first and then travels back to the beginning and this distance is counted in total distance even though no service is processed in the traverse.

=================================

3. How to compile and run this program
To compile the code use:
javac main.java

To run the code use:
java main <head>

Example:
java main 2500

=================================

4. Provide a snapshot of a sample run

prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab3$ javac main.java 
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab3$ java main 200
Time using SSTF scheduling: 5238
Time using C-SCAN scheduling: 9994
Time using C_LOOK scheduling: 9984
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab3$ java main 200
Time using SSTF scheduling: 9788
Time using C-SCAN scheduling: 9973
Time using C_LOOK scheduling: 9959
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab3$ java main 2500
Time using SSTF scheduling: 7490
Time using C-SCAN scheduling: 9991
Time using C_LOOK scheduling: 9979
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab3$ java main 2500
Time using SSTF scheduling: 7484
Time using C-SCAN scheduling: 9994
Time using C_LOOK scheduling: 9976
