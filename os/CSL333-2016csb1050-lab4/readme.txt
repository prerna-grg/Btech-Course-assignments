Submitter name: Prerna Garg
Roll No.: 2016csb1050
Course: CSL333

=================================

1. What does this program do
This is a C program that implements a client server application for the following task.
a) The client request currency conversion from the server.
b) The server serves the request by making a HTTP GET request to an external service.

=================================

2. A description of how this program works (i.e. its logic)
The server checks whether a client has approached for a new conversion. On receiving the server makes a "wget ... " call and fetches the result and sends it to the client. It also prints the output of the conversion to the console. 

=================================

3. How to compile and run this program

gcc -o server server.c
./server

gcc -o client client.c
./client

Now enter the currency code you want to convert.

=================================

4. Provide a snapshot of a sample run

******************************* CLIENT SIDE *******************************************

prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab4$ gcc -o client client.c 
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab4$ ./client 
You can press Ctrl-C anytime you want to exit.
[2018-11-19 19:45:48] Currency code (e.g. USD, GBP, etc.): USD
[2018-11-19 19:45:50] Waiting for server’s response...
[2018-11-19 19:45:53] Conversion rate wrt INR: 0.013966

[2018-11-19 19:45:58] Currency code (e.g. USD, GBP, etc.): INR
[2018-11-19 19:45:59] Waiting for server’s response...
[2018-11-19 19:46:2] Conversion rate wrt INR: 1

[2018-11-19 19:46:2] Currency code (e.g. USD, GBP, etc.): TEST
[2018-11-19 19:46:5] Waiting for server’s response...
[2018-11-19 19:46:8] Conversion rate wrt INR: FAILED

[2018-11-19 19:46:8] Currency code (e.g. USD, GBP, etc.): GBP
[2018-11-19 19:46:20] Waiting for server’s response...
[2018-11-19 19:46:23] Conversion rate wrt INR: 0.010871

******************************* SERVER SIDE *******************************************

prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab4$ gcc -o server server.c 
prerna@prerna-pc:~/Desktop/semester5/os/CSL333-2016csb1050-lab4$ ./server 
You can press Ctrl-C anytime you want to exit.
[2018-11-19 19:45:45] Waiting for next request...

[2018-11-19 19:45:50] Request received for: USD
[2018-11-19 19:45:50] Contacting Web service...
[2018-11-19 19:45:52] INR_USD conversion is 0.013966.

[2018-11-19 19:45:52] Waiting for next request...

[2018-11-19 19:46:0] Request received for: INR
[2018-11-19 19:46:0] Contacting Web service...
[2018-11-19 19:46:2] INR_INR conversion is 1.

[2018-11-19 19:46:2] Waiting for next request...

[2018-11-19 19:46:6] Request received for: TEST
[2018-11-19 19:46:6] Contacting Web service...
[2018-11-19 19:46:8] Could not fetch the conversion

[2018-11-19 19:46:8] Waiting for next request...
[2018-11-19 19:46:21] Request received for: GBP
[2018-11-19 19:46:21] Contacting Web service...
[2018-11-19 19:46:23] INR_GBP conversion is 0.010871.
