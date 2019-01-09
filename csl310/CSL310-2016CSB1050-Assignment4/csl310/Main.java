//package csl310;

//import csl310.db.DataAccessLayer;
import java.io.*;
import java.sql.*;
import java.util.*;
import java.io.Console;
import java.util.regex.*;
import java.util.Scanner;
import java.sql.SQLException;
import java.util.List;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

import java.util.Date;
public class Main {

    private DataAccessLayer dal;

    public Main(){
    	try {
    	System.out.print("\nEnter DB login: "); // user input for username
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String user = br.readLine(); // username
		Console cnsl = null;
		cnsl = System.console(); 
		char[] pwd = cnsl.readPassword("Enter DB password: "); // password
		String pass = String.valueOf(pwd);
		String url = "jdbc:mysql://localhost:3306/myBank" ; // link to database
			this.dal = new DataAccessLayer(url,user,pass);
		} catch (SQLException ex) {
			Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
		} catch (IOException ex) {
			Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
		}
    }
    /* Makes Basic function calls to carry out the work */
    public static void main(String[] args) {
    	if(args.length != 1){
	    	System.out.println("Use: java -cp mysql-connector.jar:. Main -i or -q"); // use instructions
	    	return ;
    	}
        Main app = new Main(); // constructing main 
        // if insertion option selected 
    	if(args[0].equalsIgnoreCase("-i")){
    		int check = app.dal.checkData();
    		if(check==0){
    			System.out.println("50 users and corresponding data already present."); // data already exists
    			return;
    		}
    		/* Generate new random data and add to database */
    		int cities = app.dal.getNewDummyAddress();
			app.dal.addNewContacts(cities);
			app.dal.addNewUsers();
			app.dal.addNewBankAccounts();
			app.dal.addNewTransactions();
    	}
        // if query option selected 
    	else if(args[0].equalsIgnoreCase("-q")){
    		/* User input for type of query */
    		Scanner scan = new Scanner(System.in);
    		System.out.println("Enter 1 to print the transactions recorded for a given account between given two dates.");
    		System.out.println("Enter 2 to print Category wise spending of a given person in a given month.");
    		System.out.println("Enter 3 to print Category wise spending in a given month by all persons (taken together) who live in a given city.\nYour Selection: ");
    		
	        int num = scan.nextInt();
	        try{
			    if(num==1){
			    	/* User input for query arguments */
			    	System.out.print("Enter AccountID: ");
			    	Scanner scan2 = new Scanner(System.in);
			    	int ID = scan2.nextInt();
			    	System.out.print("Enter start date Format(yyyy-mm-dd): ");
			    	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
					String start = br.readLine();
			    	System.out.print("Enter end date: Format(yyyy-mm-dd): ");
			    	br = new BufferedReader(new InputStreamReader(System.in));
					String end = br.readLine();
					/* Fetching results */
					List<TransactionDTO> output = app.dal.queryTransactions(ID, start , end );
					/* Printing Output */
					System.out.println("Results fetched for AccountID " + ID + " are:");
					for(TransactionDTO t : output){
						System.out.println(t.toString());
					}
				
			    }else if(num==2){
			    	/* User input for query arguments */
			    	System.out.print("Enter Person ID: ");
			    	Scanner sc1 = new Scanner(System.in);
			    	int ID = sc1.nextInt();
			    	System.out.print("Enter month: ");
			    	Scanner sc2 = new Scanner(System.in);
			    	int mon = sc2.nextInt();
			    	/* Fetching results */
			    	List<CategoryExDTO> output2 = app.dal.queryExpenditure1(ID,mon);
			    	/* Printing Output */
			    	System.out.println("Results fetched for PersonID " + ID + " for month: " + mon + " are:");
					for(CategoryExDTO t : output2){
						System.out.println(t.toString());
					}
			    	
			    }else if(num==3){
			    	/* User input for query arguments */
			    	System.out.print("Enter month: ");
			    	Scanner scan3 = new Scanner(System.in);
			    	int mon = scan3.nextInt();
			    	System.out.print("Enter cityName ");
			    	BufferedReader br2 = new BufferedReader(new InputStreamReader(System.in));
					String city = br2.readLine();
					/* Fetching results */
			    	List<CategoryExDTO> output3 = app.dal.queryExpenditure2(city , mon);
			    	/* Printing Output */
			    	System.out.println("Results fetched for City " + city + " for month " + mon + " are:");
					for(CategoryExDTO t : output3){
						System.out.println(t.toString());
					}
			    }else{
			    	System.out.println("Invalid query");
			    	return;
			    }
			}catch (IOException ex) {
				Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
			}

    	}else{
    		System.out.println("Use: java -cp mysql-connector.jar:. Main -i or -q");
	    	return ;
    	}
    }
}
