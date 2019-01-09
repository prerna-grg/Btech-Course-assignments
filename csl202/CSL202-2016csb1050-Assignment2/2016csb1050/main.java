/*
	To run the code use:
	javac main.java
	java -cp .:./algorithms/2016csb1050.jar main
*/

import java.io.*;
import algorithms.SortingAlgorithms;
import algorithms.SearchAlgorithms;
import algorithms.GetAlgorithmFactory;
import java.util.Random;
import java.util.Scanner;

public class main{  
    public static void main(String args[])throws IOException{
    	//Iniitialising an array for sort/search
    	int arr[] = new int[1000];
    	Random randomNum = new Random();
    	for(int i=0 ; i<1000 ; i++){
    		arr[i] = randomNum.nextInt(1000);
    	}
    	System.out.println("An array of 1000 random number initialised");
    	
    	//Initialsing an instance of factory class
		GetAlgorithmFactory algorithmFactory = new GetAlgorithmFactory();  
        
		System.out.print("Enter the name of desired Sort (bubble/insertion/selection): ");  
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));  
		String algoName = br.readLine();
		
		//Using factory to instantiate a sorting algorithm
		SortingAlgorithms a = algorithmFactory.getSortAlgo(algoName);
		if(a!=null){
			a.print();
			a.sort(arr);
			System.out.print("Enter the name of desired Search(linear/binary/jump): ");  
			br = new BufferedReader(new InputStreamReader(System.in));  
			algoName = br.readLine();
			
			System.out.print("Enter number to search: ");
			Scanner input = new Scanner(System.in);
			int x = input.nextInt();
			
			//Using factory to instantiate a search algorithm
			SearchAlgorithms s = algorithmFactory.getSearchAlgo(algoName);
			if(s!=null){
				s.print();
				s.search(arr , x);
				System.out.print("\n");
			}else{
				System.out.println("Error: Invalid Search Query");
			}
		}else{
			System.out.println("Error: Invalid Sort Query");
		}
	}
}
