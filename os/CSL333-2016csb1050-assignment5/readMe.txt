Submitter name: Prerna Garg
Roll No.: 2016csb1050
Course: CSL333

=================================

1. What does this program do
This program provides a simulation for three different page replacement policies : First-In-First-Out (FIFO) , Least-Frequently-Used (LFU) and Most-Frequently-Used (MFU). The simulate.py file contains the implementation of these 3 three algorithms while the main.py file is a test file where user input is taken to run the simulation with desired parameters.


=================================
2. A description of how this program works (i.e. its logic)
FIFO: To implement this page replacement policy I have used a variable that initially starts from 0 keeps incrementing itself when a new page is added. When its value reaches the end of the page table I reinitialise it to 0 because the replacement will start in the format of queue i.e. first in first out.

MFU: Initially a new page is sequentially filled into the page table and after the end is reached the one with maximum access frequency is replaced with the new one

LFU: Initially a new page is sequentially filled into the page table and after the end is reached the one with minimum access frequency is replaced with the new one


=================================
3. How to compile and run this program
python3 main.py

The inputs should not be given as command line arguments.
They will be asked by the terminal itself after running.
