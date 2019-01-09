/*
* Name: Prerna Garg 
* EntryNo: 2016csb1050
* CSL202: Assignment 3
* Java Code to extract useful information from a jar file containing compiled java classes.
* Input: URL of jar file and path where to save the jar file, Instructions to run the code:
* $ javac JavaDownloadFileFromURL
* $ java JavaDownloadFileFromURL
*/

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.io.File;
import java.io.*;
import java.util.*;
import java.util.List;
import java.util.logging.Logger;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;
import java.util.Scanner;
import java.lang.reflect.Method;
import java.util.regex.*;

public class InferClassInfo {

    public static void main(String[] args) throws IOException,InterruptedException {
    	
    	//User Input for URL of jar file to be downloaded
    	System.out.println("\nEnter the url of the jar file to download:");
    	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));  
		String url = br.readLine();
		
		//User Input for path where the jar file is to be saved
		System.out.println("\nEnter the path to save file: --format-- /home/myFolder/myJarFile.jar ");
    	br = new BufferedReader(new InputStreamReader(System.in));  
		String path = br.readLine();
		boolean h1 = path.endsWith(".jar");
		boolean h2 = url.endsWith(".jar");
		
		//Invalid file name will corrupt the further execution of the program, the code is specific to jar files
 		if(!h1 || !h2){
			System.out.println("ERROR: Please enter file name with .jar extension");
			return;
		}
		
		// Initialising Report File
		PrintStream file = new PrintStream(new File("2016csb1050_Report.txt"));
		PrintStream console = System.out;
		System.setOut(file); // To print to file

        try {
            downloadURL(url, path);
            System.setOut(console); // To print to console
			System.out.println("The jar file has been successfully Downloaded and saved as: " + path);
			System.out.println("Writing output to 2016csb1050_Report.txt ......");
			System.setOut(file); // To print to file
            printClassNames(path);
            System.setOut(console);
            System.out.println("DONE...All observations can be found in 2016csb1050_Report.txt");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

	/* The following method downloads the file from the url given as input to the method. I have made use of Java objects URL, ReadableByteChannel and FileOutputStream for the same */
    private static void downloadURL(String urlStr, String file) throws IOException {
        URL url = new URL(urlStr);
        ReadableByteChannel rbc = Channels.newChannel(url.openStream());
        FileOutputStream fos = new FileOutputStream(file);
        fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
        fos.close();
        rbc.close();
    }
    
    /*This is the primary function for extracting all useful data from the jar file. It calls several other functions to do the same.*/
    private static void printClassNames(String path)  throws IOException,FileNotFoundException{
    	/* First I traverse the jar file and extract name of the class and store it in a list of Strings.*/
    	List<String> classNames = new ArrayList<String>();
    	List<String> origNames = new ArrayList<String>();
		ZipInputStream zip = new ZipInputStream(new FileInputStream(path));
		for (ZipEntry entry = zip.getNextEntry(); entry != null; entry = zip.getNextEntry()) {
			if (!entry.isDirectory() && entry.getName().endsWith(".class")) {
				String temp = entry.getName();
				String className = temp.replace('/','.'); //Replaced to generate formatted class name
				classNames.add(className);
				origNames.add(temp);
			}
		}
		System.out.println("The following classes were found in the jar file");
		int i=1;
		// Printing class files names
		for( String s : classNames){
			System.out.print(i + ". "); // Serial Number
			System.out.println(s);
			i++;
		}
		
		System.out.println("\nNUMBER OF METHODS IN THE JAR FILE:");
		float count=0;
		for( String s : origNames){
			int d = printClassMethodsNumber(s , path); // Function call to count methods in a class
			System.out.println(s + " = " + d);
			count += d;
		}
		float j = i;
		System.out.println("\nAVERAGE number of methods in a class is: " + count/(j-1) + "\n" );
		
		int ar[] = new int[i-1];
		i = 0;
		System.out.println("CONSTANT POOL SIZE OF ALL CLASSES:");
		for( String s : origNames){
			int d = printConstantPoolSize(s , path); // Function call to measure constant pool size of each class
			System.out.println(s+" = " + d);
			ar[i] = d;
			i++;
		}
		/* Printing the required average, maximum, minimum and standard deviation of constant pool sizes obtained*/
		printAvgMinMaxStdDev(ar , origNames); 
		
		//Final function call to find JVM instruction distribution across all classes
		printJVMinstructions(origNames , path);
    }
    
    /* This function takes input constant pool sizes and respective names of each class to generate a wel formatted output*/
    private static void printAvgMinMaxStdDev(int[] ar , List<String> args){
    	int min = 10000000 , min_index=-1;
    	int max = -1 , max_index=-1;
    	float sum=0;
    	float size = ar.length;
    	/* Sum, Min and Max */
    	for(int i=0 ; i<size ; i++){
    		sum += ar[i];
    		if(ar[i]<min){
    			min = ar[i];
    			min_index = i;
    		}
    		if(ar[i]>max){
    			max = ar[i];
    			max_index = i;
    		}
    	}
    	float avg = sum/size; // Average
    	double stdDev = 0;
    	for(int i=0 ; i<size ; i++){
    		stdDev += Math.pow(ar[i]-avg , 2);
    	}
    	stdDev /= size;
    	stdDev = Math.pow(stdDev , 0.5); // Standard Deviation
    	// Printing to file
    	System.out.println("\nAverage Constant Pool Size = " + avg);
    	System.out.println("Maximum Constant Pool Size = " + ar[max_index] + " for " + args.get(max_index));
    	System.out.println("Minimum Constant Pool Size = " + ar[min_index] + " for " + args.get(min_index));
    	System.out.println("Standard Deviation for the pool sizes = " + stdDev);
    }
    
    /* This method counts number of methods in the class */
    private static int printClassMethodsNumber(String Name , String jarFilePath){
    	Name = Name.substring(0, Name.length() - 6); // remove .class
    	int count=0;
		try{
			// Instruction to get the data about methods
			List<String> cmdList = new ArrayList<String>();
			cmdList.add("javap");
			cmdList.add("-p"); // To exclude private functions just comment this line
			cmdList.add("-cp");
			cmdList.add(jarFilePath);
			cmdList.add(Name);
			ProcessBuilder pb = new ProcessBuilder(cmdList);
			Process p = pb.start();
			// Store the output in an InputStream
			InputStream fis = p.getInputStream();
			count = DisplayClassStructure(fis); //Number of methods
		}catch(IOException e1){
			e1.printStackTrace();
		}
		return count;
	}
	
	/* The method takes an inputstream generated as an output of javap SOME_NAME.class and reads it line by line to find methods */
	private static int DisplayClassStructure(InputStream is){
		InputStream stream;
		int count=0;
		try{
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			String line;   
			while ((line = reader.readLine()) != null) {
				String rgx = "^[^(]*[(][^)]*[)][^;]*[;]"; //Regular expression to match method
				Pattern pattern = Pattern.compile(rgx);
                Matcher matcher = pattern.matcher(line);
                // If matched do:
				if(matcher.find()){
					count++;
				}
			}
			reader.close();
		}catch (FileNotFoundException e) {
			e.printStackTrace();
		}catch (IOException e) {
			e.printStackTrace();
		}
		return count;
	}
	
	/* This method runs javap -verbose SOME_NAME.class to generate the entries of the constant pool and stores the output in an InputStream which is passed to another function to count the number of entries */
	private static int printConstantPoolSize(String Name , String jarFilePath){
    	int count = 0 ;
    	Name = Name.substring(0, Name.length() - 6); // remove .class
    	try{
    		List<String> cmdList = new ArrayList<String>();
			cmdList.add("javap");
			cmdList.add("-verbose");
			cmdList.add("-cp");
			cmdList.add(jarFilePath);
			cmdList.add(Name);
			ProcessBuilder pb = new ProcessBuilder(cmdList);
			Process p = pb.start();
			InputStream fis = p.getInputStream();
			count = DisplayConstantPoolSize(fis);
    	}catch(IOException e1){
			e1.printStackTrace();
		}
		return count;
    }
    
    /* The method reads the input stream to count number of entries in the constant pool of a class */
    private static int DisplayConstantPoolSize(InputStream is){
    	InputStream stream;
		int count=0;
		try{
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			String line; 
			int flag = 0;
			while ((line = reader.readLine()) != null){
				String rgx = "Constant pool:";
				Pattern pattern = Pattern.compile(rgx);
                Matcher matcher = pattern.matcher(line);
                
				if(matcher.find()){
					flag = 1;  // Start Counting from here on
				}
				else{
					if(line.equals("{")){
						flag = 0; // End counting from here on with ensuring that it is indeed the end of pool, any '{' in any other line would not match 
						break;
					}
					if(flag == 1){
						count++;
					}
				}
			}
		}catch (FileNotFoundException e) {
			e.printStackTrace();
		}catch (IOException e) {
			e.printStackTrace();
		}
		return count;
    }
    
    /* This method is used to find top 50 instructions in terms of frequency of occurrence in the jar file */
    private static void printJVMinstructions(List<String> origNames , String jarFilePath) throws IOException{
		try{
			HashMap<String,Integer> Instructions = new HashMap<String,Integer>();
			/* HashMap to store instructions with key as instruction name and value as the occurrence frequency */
			for(String s : origNames){
				// Generate instruction to get the JVM instructions for all classfiles
				List<String> cmdList = new ArrayList<String>();
				s = s.substring(0, s.length() - 6); // remove .class
				cmdList.add("javap");
				cmdList.add("-c");
				cmdList.add("-p"); // comment to remove private methods
				cmdList.add("-cp");
				cmdList.add(jarFilePath);
				cmdList.add(s);
				ProcessBuilder pb = new ProcessBuilder(cmdList);
				Process p = pb.start();
				InputStream fis = p.getInputStream(); // Store output in InputStream
				BufferedReader reader = new BufferedReader(new InputStreamReader(fis));
				String line; 
				int flag = 0;
				while ((line = reader.readLine()) != null){
					String rgx = "[\\s]*[0-9]+:.*"; //Regular expression to check if the line is a JVM Instruction
					Pattern pattern = Pattern.compile(rgx);
			        Matcher matcher = pattern.matcher(line);
			        String[] splited = line.split("\\s+");
			        
					if(matcher.find()){
						String insName = splited[2];
						String rgx2 = "^[0-9]+";
						Pattern pattern2 = Pattern.compile(rgx2);
					    Matcher matcher2 = pattern2.matcher(insName);
					    if(matcher2.find())continue; //Invalid matches of type 89: 90 , 90 is not a instruction
						if(Instructions.containsKey(insName)){
							int i = Instructions.get(insName) + 1;
							Instructions.remove(insName);
							Instructions.put(insName , i);
						}else{
							Instructions.put(insName , 1);
						}
					}
				}
			}
			/* Retreive all entries from HashMap for further processing */
			int ins = Instructions.size();
			Object arS[] = new Object[ins];
			Object arI[] = new Object[ins];
			int start=0;
			Iterator itc = Instructions.entrySet().iterator();
			while (itc.hasNext()) {
				HashMap.Entry pair = (Map.Entry)itc.next();
				arS[start] = pair.getKey();
				arI[start] = Instructions.get(arS[start]);
				itc.remove();
				start++;
			}
			int max = -1;
			int maxi = -1;
			int make = 0;
			/* If total instructions are less than 50 : */
			if(ins<50)make = ins;
			else make = 50;
			String arSo[] = new String[make];
			int arIo[] = new int[make];
			start = 0;
			// Selection Sort to get top 50 and store their names and respective values in array
			// O(n) solution because it runs < 50*n times
			for(int i=0 ; i<make ; i++){
				for(int j=0 ; j<ins ; j++){
					int h = (Integer)arI[j];
					if(h>max){
						max = h;
						maxi = j;
					}
				}
				String hs = (String)arS[maxi];
				arSo[start] = hs;
				arIo[start] = max;
				arI[maxi] = -1;
				start++;
				maxi = -1;
				max = -1;
			}
			/* Print formatted output to file */
			System.out.println("\n\nJVM Instruction Distribution: ");
			System.out.println("++++++++++++++++++++++++++++++++++++");
			int g=0;
			while (g!=start) {
				System.out.format("%-20s |    %d \n" , arSo[g] ,arIo[g]);
				g++;
			}
		}
		catch (IOException e) {
			e.printStackTrace();
		}
    }
}
