Instructions to run the code:

$ javac JavaDownloadFileFromURL
$ java JavaDownloadFileFromURL

URL and path to save jar will be given as Input through command line

Output will be stored as a report names 2016csb1050_Report.txt

Report Format:
1) Number of classes present in the jar file
2) Number of methods present in each class in the jar file
3) Average number of methods
4) Constant pool size of each class
5) Average/Maximum/Minimum/Standard Deviation of pool sizes for the jar file
6) JVM Instruction Distribution for the jar file i.e. instructions produced across all classes

Note: aload_0 and aload_1 or any such other instructions have been taken different because their opcodes are entirely different
Note: In order to exclude private methods comment the line: cmdList.add("-p"); this will eliminate private methods from analysis

Algorithm Working:

1) Download Jar file From URL
2) Use ProcessBuilder to run commands to get useful information from javap, I have given jar file also as an input to the instruction to avoid extracting the jar file.
3) Store the result of process in an InputStream
4) Read the inputSTream line by line and find useful information using regular expressions or string operations
5) For instructions I have created a HashMap to store the name and correspinding frequency, as and when an instruction is found its frequency is updated into the map if it already exists else a new element is added to it
6) Retreive entries from map and store in an array to sort and print top 50 instructions, This method makes sorting O(n) as the for loops run 50*n times where n is the number of instructions found in all classes collectively.
7) I have used StringBuilder to generate the formatted output and stored in a report.
