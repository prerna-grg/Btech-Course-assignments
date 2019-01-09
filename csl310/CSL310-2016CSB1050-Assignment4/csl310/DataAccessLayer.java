//package csl310.db;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.io.*;
import java.util.Date;
import java.sql.*;
import java.util.*;
import java.util.Scanner;
import java.util.List;
import java.util.Random;
import java.text.*;
import java.util.Calendar;
import java.util.GregorianCalendar;

public class DataAccessLayer {
	
	/* Reading properties from queries.properties file */
	private Connection conn = null;
	public static final String SQL_INSERT_ACC = "account.insert.sql";
	public static final String SQL_INSERT_CON = "country.insert.sql";
	public static final String SQL_INSERT_ST = "state.insert.sql";
	public static final String SQL_INSERT_CT = "city.insert.sql";
	public static final String SQL_INSERT_CONT = "contact.insert.sql";//contacts
	public static final String SQL_INSERT_BACC = "bankacc.insert.sql";
	public static final String SQL_SELECT_ACC = "select.trans.sql";
	public static final String SQL_INSERT_TRAN = "create.transaction.sql";
	public static final String SQL_UPDATE_DTRAN = "amount.debit.sql";
	public static final String SQL_UPDATE_CTRAN = "amount.credit.sql";
	public static final String SQL_SELECT_TRAN = "select.trans.date";
	public static final String SQL_SELECT_EXP1 = "select.person.city";
	public static final String SQL_SELECT_EXP2 = "select.trans.city";
	public static final String SQL_CHECK_DATA = "check.data.sql";
	private Properties queries = new Properties();

	/* Establish Connection */
	public DataAccessLayer(String dbUrl , String user , String pass) throws SQLException {
		try{
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection(dbUrl , user , pass); // user credentials to access database
		}catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		try {    
			queries.load(DataAccessLayer.class.getResourceAsStream("queries.properties"));
		}catch (IOException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
	}
    /* The function checks if the database already has data */
    public int checkData(){
		try{	
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_CHECK_DATA));
			ResultSet rs = ps.executeQuery();
			while(rs.next()){
				return 0; // row found means data exists
			}
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		return 1;
    }
    
    /* This function executes the first query i.e. print the transactions recorded for a given account between given two dates.*/
    public List<TransactionDTO> queryTransactions(int ID , String d1 , String d2){
    	List<TransactionDTO> output = new ArrayList<TransactionDTO>();
    	try {
			// 2. Create a SQL stmt
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_SELECT_TRAN));
			// set the arguments required
			ps.setInt(1,ID);
			ps.setString(2,d1);
			ps.setString(3,d2);
			ResultSet rs = ps.executeQuery();
			
			while(rs.next()){
				/* Store the outputs in Data transfer objects to be given to main */
				TransactionDTO temp = new TransactionDTO();
				temp.TransactionID = rs.getInt("TransactionID");
				temp.TransactionType = rs.getString("TransactionType");
				temp.TransactionDatetime = rs.getDate("TransactionDatetime");
				temp.Amount = rs.getInt("Amount") ;
				temp.AccountID = rs.getInt("AccountID");
				temp.Category = rs.getString("Category");
				temp.Remarks = rs.getString("Remarks");
				output.add(temp);
			}
    	}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		return output; //return to main
    }
    
    /* This function executes the second query i.e. print Category wise spending of a given person in a given month. */
    public List<CategoryExDTO> queryExpenditure1(int ID, int month){
    	List<CategoryExDTO> output = new ArrayList<CategoryExDTO>();
    	try {
			// 2. Create a SQL stmt
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_SELECT_EXP1));
			// set the arguments required
			ps.setInt(1,ID);
			ps.setInt(2,month);
			ResultSet rs = ps.executeQuery();
			
			while(rs.next()){
				/* Store the outputs in Data transfer objects to be given to main */
				CategoryExDTO temp = new CategoryExDTO();
				temp.Category = rs.getString("Category");
				temp.Expenditure = rs.getInt("Expenditure");
				output.add(temp);
			}
    	}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		return output; //return to main
    }
    
    /* This function executes the third query i.e. print Category wise spending in a given month by all persons (taken together) who live in a given city.*/
    public List<CategoryExDTO> queryExpenditure2(String cityName, int month){
    	List<CategoryExDTO> output = new ArrayList<CategoryExDTO>();
    	try {
			// 2. Create a SQL stmt
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_SELECT_EXP2));
			// set the arguments required
			ps.setString(1,cityName);
			ps.setInt(2,month);
			ResultSet rs = ps.executeQuery();
			
			while(rs.next()){
				/* Store the outputs in Data transfer objects to be given to main */
				CategoryExDTO temp = new CategoryExDTO();
				temp.Category = rs.getString("Category");
				temp.Expenditure = rs.getInt("Expenditure");
				output.add(temp);
			}
    	}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		return output; //return to main
    }
    
    /* The function add some random 50 users to the database */
    public void addNewUsers() {
    	AccountHolder temp[] = getNewDummyNames(); // get random 50 names for the database
    	Random random = new Random();
        try {
			// 2. Create a SQL stmt
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_ACC));
			int i=1;
			int con=1;
			for (AccountHolder a : temp ){
				RandomDate rndd = new RandomDate(); // get random birth date
				Date DOB = rndd.getDate(1890,1900);
				RandomPAN rndp = new RandomPAN(); // get random PAN card number
				String s = rndp.getPAN();
				NumberFormat nf = new DecimalFormat("0000");
				s += nf.format(i);
				s += 'C';
				RandomContact rndc = new RandomContact(); // get random contact ID
				String n = rndc.getCon();
				// set the data 
				ps.setString(1,s);
				ps.setString(2,a.First_Name);
				ps.setString(3,a.Last_Name);
				ps.setDate(4, new java.sql.Date(DOB.getTime()));
				ps.setInt(5,con);
				con = con + 1;
				i = i+1;
				// add to the database 
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert user failed!!");
		        }
			}
			System.out.println("New Users Added");
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}

	}
	
	
	/* Generates random bank accounts 1 for each user and randomly sets their values */
	public void addNewBankAccounts() {
    	Random random = new Random();
        try {
			// 2. Create a SQL stmt
			int start = 1900;
			int stop = 1900;
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_BACC));
			for ( int i=1 ; i<=50 ; i++ ){
				RandomDate rndd = new RandomDate(); // random opening date
				Date Open = rndd.getDate(start,stop);
				ps.setDate(1, new java.sql.Date(Open.getTime()));
				ps.setInt(6,random.nextInt(500000) + 100000); // random amount
				Date Close = rndd.getDate(1700,stop); // random closing date 
				start = start + 1; 
				stop = stop + 1;
				String status;
				/* Random decision for active vs dormant account ... more probabilty given to active */
				if(Close.getTime() - Open.getTime() > 0){
					status = "Dormant";
					ps.setDate(2,new java.sql.Date(Close.getTime()));
					ps.setInt(6,0);
				}else{
					status = "Active";
					ps.setString(2,null);
				}
				// set the data
				ps.setString(3,status);
				ps.setInt(4,i);
				ps.setString(5 , "Savings");
				
				// insert the data 
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert user failed!!");
		        }
			}
			System.out.println("New Bank Accounts Generated");
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
	}

	/* Generates random transactions for user accounts in the following fashion .. the accounts are created at random but serialized dates .. for account 1 no transaction is possible .. for account 2 .. one transaction is done with account1 .. for account 3 .. 2 transactions are done .. with account 2 and account 1 ... account 4 generates 3 transactions with account 3,2 and 1 and so on ...
	This step continues for next 10 days.
	*/
	public void addNewTransactions(){
    	Random random = new Random();
    	List<String> Categories = new ArrayList<String>(); // transaction categories
    	try{
			FileReader fileReader = new FileReader("transaction_categories.txt");
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			String line;
			while( (line = bufferedReader.readLine()) != null){
				Categories.add(line);
			}
		}catch(FileNotFoundException ex) {
			System.out.println("Missing file transaction_categories.txt");
		}catch(IOException e) {
			System.out.println("Missing file transaction_categories.txt");
		}
		
		int size = Categories.size();
		int count=0;
		System.out.println("Generating Transactions...");
	    try {
	    	for(int i=1 ; i<50 ; i++){
	    		int j = i-1;
				List<BankAccount> accounts = new ArrayList<BankAccount>();
				PreparedStatement ps=conn.prepareStatement(queries.getProperty(SQL_SELECT_ACC));
				ResultSet rs = ps.executeQuery();
				while(rs.next()){
					BankAccount temp = new BankAccount();
					temp.AccountID = rs.getInt("AccountID");
					temp.ODate = rs.getTimestamp("OpeningDate");
					temp.CDate = rs.getTimestamp("ClosingDate");
					temp.CBL = rs.getInt("CurrentBalance");
					accounts.add(temp);
				}
				for(int as = 0 ; as<5 ; as++){
					for ( int k=j ; k>=0 ; k-- ){
						if(accounts.get(k).CDate!=null)continue; // if account closed forget it
						int getTransDate = as; 
						ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_TRAN));
						int temp_amount = accounts.get(i).CBL / (i+1) ;
						if(temp_amount <= 0)continue;
						// set data 
						ps.setString(1,"Debit");
					
						Date currDate = new java.sql.Date(accounts.get(i).ODate.getTime());
						DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
		          		String dt = df.format(currDate);
		          		
		          		Calendar c = Calendar.getInstance();
						c.setTime(currDate);
						int day = c.get(Calendar.DAY_OF_MONTH);
		          		int month = c.get(Calendar.MONTH);
		          		int year = c.get(Calendar.YEAR);
						GregorianCalendar startdate = new GregorianCalendar(year,month,day);
						startdate.add(GregorianCalendar.DATE, getTransDate);
				        Date d = startdate.getTime();

						ps.setDate(2,new java.sql.Date(d.getTime()));				
						ps.setInt(3,temp_amount);
						ps.setInt(4,accounts.get(i).AccountID);
						ps.setString(5,Categories.get(random.nextInt(size)));
						ps.setString(6,"Successful :)");		
						// set auto commit to false as transaction needs to be done in 2 accounts
						conn.setAutoCommit(false);
						// execute
						int rows1 = ps.executeUpdate();
						if (rows1 != 1) {
							System.out.println(">>>>> Transaction failed!!");
						}
						// set data 
						ps.setString(1,"Credit");
						ps.setInt(4,accounts.get(k).AccountID);
						// execute
						rows1 = ps.executeUpdate();
						if (rows1 != 1 ) {
							System.out.println(">>>>> Transaction failed!!");
						}
						ps = conn.prepareStatement(queries.getProperty(SQL_UPDATE_DTRAN));
						ps.setInt(1,temp_amount);
						ps.setDate(2, new java.sql.Date(d.getTime()) );
						ps.setInt(3,accounts.get(i).AccountID);
						// update corresponding data in last transaction date in bank account table
						rows1 = ps.executeUpdate();
						if (rows1 != 1 ) {
							System.out.println(">>>>> Transaction failed!!");
						}
					
						ps = conn.prepareStatement(queries.getProperty(SQL_UPDATE_CTRAN));
						ps.setInt(1,temp_amount);
						ps.setDate(2,new java.sql.Date(d.getTime()));
						ps.setInt(3,accounts.get(k).AccountID);
						// update corresponding data in last transaction date in bank account table
						rows1 = ps.executeUpdate();
						if (rows1 != 1 ) {
							System.out.println(">>>>> Transaction failed!!");
						}
						// commit the changes
						conn.commit();
						count++; // number of total transactions
						accounts.clear();
						ps=conn.prepareStatement(queries.getProperty(SQL_SELECT_ACC));
						rs = ps.executeQuery();
						// get the updated data for further processing
						while(rs.next()){
							BankAccount temp = new BankAccount();
							temp.AccountID = rs.getInt("AccountID");
							temp.ODate = rs.getDate("OpeningDate");
							temp.CBL = rs.getInt("CurrentBalance");
							accounts.add(temp);
						}
					}
				}
			}
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
			//conn.rollback();
			System.out.println("!!!! TRANSACTION ROLLEDBACK.");
		}finally {
	        //conn.setAutoCommit(true);
	    }
	    System.out.println(count + " new Transactions Added");
	    System.out.println(2*count + " entries entered in Database");
	}
	
	/* Generates random contacts, postal codes and street names */
	public void addNewContacts(int cities) {
    	Random random = new Random();
        try {
			// 2. Create a SQL stmt
			int j = 1;
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_CONT));
			for (int i=0 ; i<50 ; i++){
				if(j==6)j=1;
				RandomContact rndc = new RandomContact(); // random number 
				String n = rndc.getCon();
				RandomPostal p = new RandomPostal();
				String post = p.getPost();
				ps.setString(1,"Agarwal Colony, India"); // random street
				ps.setInt(2,j);
				ps.setString(3,post);
				ps.setString(4, n);
				j++;
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert post failed!!");
		        }
			}
				
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		System.out.println("New Contacts Added");
	}
	
	/* Generates random addresses i.e. combinations of cities + states + countries */
	public int getNewDummyAddress() {
		Random random = new Random();
		ContactInformation temp[] = new ContactInformation[50];
		String fileName = "cities.txt"; // names of cities
		List<String> Cities = new ArrayList<String>();
		List<String> States = new ArrayList<String>();
		List<String> Countries = new ArrayList<String>();
		HashMap<String,Integer> CountryIDs = new HashMap<String,Integer>();
		try{
			FileReader fileReader = new FileReader(fileName);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			String line;
			while( (line = bufferedReader.readLine()) != null) {
				Cities.add(line); // list of cities
			}	
			fileName = "states.txt"; // names of states
			fileReader = new FileReader(fileName);
			bufferedReader = new BufferedReader(fileReader);
			while( (line = bufferedReader.readLine()) != null) {
				States.add(line); // list of states
			}
			fileName = "countries.txt"; // name of countries
			fileReader = new FileReader(fileName);
			bufferedReader = new BufferedReader(fileReader);
			while( (line = bufferedReader.readLine()) != null) {
				Countries.add(line); // list of countries
			}
		}catch(FileNotFoundException ex) {
			System.out.println("Missing files");
		}catch (IOException e) {
			e.printStackTrace();
		}
		int i=0;
		int cn_c = 0;
		int st_c = 0;
		int ci_c = 0;
		/* The following adds countries and remembers the count of them */
		try {
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_CON));
			for (String cnt : Countries ){
				ps.setString(1,cnt);
				cn_c = cn_c +1;
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert country failed!!");
		        }
			}
				
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		
		/* the following snippet adds states and randomly assigns country IDs to them*/
		try {
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_ST));
			int CID = 0;
			for (String st : States ){
				CID = random.nextInt(cn_c) + 1; // random country ID
				ps.setString(1,st);
				ps.setInt(2,CID);
				st_c = st_c +1;
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert state failed!!");
		        }
			}	
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		
		/* the following snippet adds cities and randomly assigns state IDs to them*/
		try {
			PreparedStatement ps = conn.prepareStatement(queries.getProperty(SQL_INSERT_CT));
			int SID = 0;
			for (String ct : Cities ){
				SID = random.nextInt(st_c) + 1; // random state ID
				ps.setString(1,ct);
				ps.setInt(2,SID);
				ci_c = ci_c +1;
				int rows = ps.executeUpdate();
		        if (rows != 1) {
		            System.out.println(">>>>> Insert city failed!!");
		        }
			}	
		}catch (SQLException ex) {
			Logger.getLogger(DataAccessLayer.class.getName()).log(Level.SEVERE, null, ex);
		}
		System.out.println("New Addresses Generated");
		return ci_c; // return the number of cities
    }
    
    /* Generates random Dummy Names for account users */
    private AccountHolder[] getNewDummyNames() {
		Random rnd = new Random();
		AccountHolder temp[] = new AccountHolder[50]; // data holder
		String fileName = "dummy_sur_names.txt"; // sur names file
		try{
			FileReader fileReader = new FileReader(fileName);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			
			int i=0;
			String line;
			while( i<50 ){
				while( (line = bufferedReader.readLine()) != null) {
					if(i>=50)break;
					temp[i] = new AccountHolder();
					temp[i].Last_Name = line;
					i++;
				}
				fileReader = new FileReader(fileName);
				bufferedReader = new BufferedReader(fileReader);
			}
			fileName = "dummy_names.txt"; // names file
			fileReader = new FileReader(fileName);
			bufferedReader = new BufferedReader(fileReader);
			i=0;
			while( i<50 ){
				while( (line = bufferedReader.readLine()) != null) {
					if(i>=50)break;
					temp[i].First_Name = line;
					i++;
				}
				fileReader = new FileReader(fileName);
				bufferedReader = new BufferedReader(fileReader);
			}
		}catch(FileNotFoundException ex) {
			System.out.println("Missing files");
		}catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("New Names Generated");
		return temp;
    }
}

