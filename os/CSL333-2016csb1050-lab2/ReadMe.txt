Submitter name: Prerna Garg
Roll No.: 2016CSB1050
Course: CSL333

=================================

1. What does this program do
This program tests the read/write efficiency of RAM while dealing with large mega bytes of data. The comparison is done between reading one byte at a time versus reading k bytes at a time where k varies in {10, 20, 30, 40, 50, 60} and the test array size varies in  {10, 20, 40, 80, 160, 320, 640, 1280} MB . Total of 48 cases are tested and the resulting times are given as output to the console.

=================================

2. A description of how this program works (i.e. its logic)
For each N,K pair this program allocates memory of size equivalent to N MegaBytes on the heap and assigns it to a char pointer because it's every element will be of 1 byte. Test A is performed by assigning 'a' to each element of the array. Test B is performed using memset for K bytes at a time. Test C is performed by reading one byte of the array into a temporary variable. Test D is performed using memcpy for a temporary variable of length K bytes. Time is measured using clock() command.

=================================

3. How to compile and run this program
To compile the code use:
gcc -o m memtest.c

To run the code use:
./m

=================================

4. Explanation of the outputs:
The speed obtained by reading/writing more than one byte at a time was significantly larger than reading/writing the data byte by byte. The possible reasons to this is that each time we request a read/write operation the memory manager "seeks" the desired location first and then reads the data. The seek time significantly affects the overall time needed to read/write. When we are performing the task byte by byte this seek operation is carried out for every byte but if we do this in chunks of bytes then for one chunk only one seek is required and number of seeks reduce by the factor of chunk/block size. This is the major reason that reading/writing in chunks/blocks of bytes is a lot faster than doing the same task byte by byte.

The best performance was observed with K = 60 ( sometimes 50 ) which implies block size of 50-60bytes gives the best read/write performance on arrays of large sizes.

Here is a Sample run of the program: (Individual case results have been omitted)
For N = 10 MB
Maximum Read Speed = 9920.634921 for K = 60
Maximum Write Speed = 10010.010010 for K = 60

For N = 20 MB
Maximum Read Speed = 11350.737798 for K = 60
Maximum Write Speed = 10065.425264 for K = 60

For N = 40 MB
Maximum Read Speed = 11550.678602 for K = 60
Maximum Write Speed = 9898.539965 for K = 50

For N = 80 MB
Maximum Read Speed = 12059.089539 for K = 60
Maximum Write Speed = 11569.052784 for K = 60

For N = 160 MB
Maximum Read Speed = 12050.007531 for K = 60
Maximum Write Speed = 11325.028313 for K = 60

For N = 320 MB
Maximum Read Speed = 11799.845127 for K = 60
Maximum Write Speed = 11686.082606 for K = 60

For N = 640 MB
Maximum Read Speed = 12316.692968 for K = 60
Maximum Write Speed = 11666.697049 for K = 60

For N = 1280 MB
Maximum Read Speed = 10726.197060 for K = 60
Maximum Write Speed = 11792.018278 for K = 60

Maximum Read Speed = 12316.692968 for N = 640 and K = 60
Maximum Write Speed = 11792.018278 for N = 1280 and K = 60

As we can see above K = 60 exhibits the best performance for both the operations.
The value of N is variable which is right because essentially we are doing the same operations on everything. So roughly time taken to do N operations is double the time taken to do N/2 operations and as a result the speed obtained remains same (roughly) across different values of N but changes significantly with K.
