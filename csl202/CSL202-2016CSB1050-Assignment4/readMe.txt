Instructions to run the code:

javac -cp activation.jar:javax.mail.jar:. main_top.java
java -cp activation.jar:javax.mail.jar:. main_top

To successfully send emails please do not use IIT Ropar ethernet as ports have been blocked. You may use any other hotspot.
Also make sure history_info.txt exists. The file does both read and write operations simultaneously. Explicit creation through different threads can cause errors. Hence it should exist.
Make sure you have both the jar files in the same directory.

The model has been explained in detail in design document.
