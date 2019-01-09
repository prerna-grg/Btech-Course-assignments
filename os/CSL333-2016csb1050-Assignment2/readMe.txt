Prerna Garg
2016csb1050
CSL333: Assignment 2

To run the code Please follow the given instructions:

1) Ensure that the file is in a folder that has dev folder at the same path.
2) To execute, compile the file using
javac getNthNum.java

3) To run, use
java getNthNum N number_of_threads device_type compute_delay boot_delay
Note: Last two arguments are optional
Default is 3 and 250 in milliseconds

Working/Explanation of the logic of the code:
I have defined 3 classes in getNthNum.java
1) 
	a) "myDataStruct" has 3 components. A queue Q , a priority queue PQ and a hahmap M.
	b) "MyThread" is an implementation of Runnable class and contains the code thread performs
	c) "getNthNum" is the main class that reads arguments, creates threads and hence prints the desired output.

2) The base is initialised to 2, i.e.
	Q = [2]
	PQ = []
	M = [0:2]
3) 2 is removed from the queue and added to PQ
4) As soon as the thread who took the base 2 is done, it's numbers are pushed to Q. Note that head of PQ stores the base corresponding to which the numbers will be added first. Once added the first number is removed from the queue (PQ) and the next base's thread is awaited. Meanwhile the free threads keep awaiting for numbers in Q so that they can pick up their bases and compute.
5) My Optimisation:
--> If a number is added to the map only after it is visited we would be wasting a lot of computations. Once the numbers corresponding to a base let's say b have been pushed to Q they will be used as base in the same order. Therefore we can push to the set here itself and save computations and stop computing once the map reaches the desired size.


Example for Real device:

prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 10 real 1 10
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 10
Used real device.............: true
Time taken...................: 2.484 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 16897 time


prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 100 real 1 10
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 100
Used real device.............: true
Time taken...................: 0.549 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 17998 time


prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 150 real 1 10
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 150
Used real device.............: true
Time taken...................: 0.566 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 18658 time


Example for UnReal device:
prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 10 unreal
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 10
Used real device.............: false
Time taken...................: 0.056 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 17800 time


prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 100 unreal
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 100
Used real device.............: false
Time taken...................: 0.464 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 18438 time


prerna@prerna-pc:~/Desktop/semester5/os/Assignment2/CSL333-2016csb1050-Assignment2$ java getNthNum 5000 150 unreal
----------------------------------------
RESULTS SUMMARY
----------------------------------------
Target Count (n).............: 5000
Number of threads............: 150
Used real device.............: false
Time taken...................: 0.654 sec
Resulting number.............: 1143957738
Device Invoked (approx)......: 18783 time

