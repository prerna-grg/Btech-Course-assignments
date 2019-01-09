/*
* Name: Prerna Garg 
* EntryNo: 2016csb1050
* CSL310: Assignment 3
* Java Code to extract useful information from a database.
* Input: classpath to mysqlconnector jar file and Mysql URL of a database, Instructions to run the code:
* $ javac getDatabaseMetaData.java
* $ java -cp ./mysql-connector.jar:. getDatabaseMetaData jdbc:mysql://localhost:3306/sakila
*/

import java.io.*;
import java.sql.*;
import java.util.*;
import java.io.Console;
import java.util.regex.*;

public class getDatabaseMetaData{
	/* The function establishes connection to the driver and accesses the database to extract useful imformation out of it
	   and prints the results in a well formatted format. */
	public static void main(String args[]) throws Exception {
		if(args.length != 1){
			System.out.println("Error!! Usage: java -cp ./mysql-connector.jar:. getDatabaseMetaData mysql-link-to-database");
			return;
		}
		try{
			Class.forName("com.mysql.jdbc.Driver");
			/* User Input for username and password to access mysql databases */
			System.out.print("\nEnter DB login: ");
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			String user = br.readLine(); // username
			
			/* Hidden password to support security */
			Console cnsl = null;
			cnsl = System.console();
			char[] pwd = cnsl.readPassword("Enter DB password: "); // password
			String pass = String.valueOf(pwd);
			
			/* Getting the connection to the driver and the database */
			Connection con = DriverManager.getConnection(args[0], user , pass); 
			String dataBaseName = args[0];

			/* Extract name of the database */
			StringBuilder str = new StringBuilder();
			for(int p= dataBaseName.length()-1 ; p>=0 ; p--){
				char c = dataBaseName.charAt(p);
				if( c == '/' ){
					break;
				}else{
					str.insert(0,c);
				}
			}
			dataBaseName = str.toString();
			
			/* Get the metadata of the database */
			DatabaseMetaData md = con.getMetaData();
			/* Get the tables of the database from the metadata */
			ResultSet rs = md.getTables(null, null, "%", null);
			int no_of_tables=0;
			List<String> tableNames = new ArrayList<String>();
			
			/* Finding the names of all tables present in the database -- Views excluded */
			while (rs.next()) {
				String o = rs.getString(4);
				boolean ob = o.equalsIgnoreCase("TABLE");
				if(ob){
					tableNames.add(rs.getString(3));
					no_of_tables++;
				}
			}
			
			/* Arrays storing table metadata */
			int[] no_of_cols = new int[no_of_tables]; // Number of columns
			int[] no_of_rows = new int[no_of_tables]; // Number of rows
			int[] no_of_fk = new int[no_of_tables]; // Number of foreign keys 
			int[] no_of_index = new int[no_of_tables]; // Number of indexes 
			int[] no_of_autoInc = new int[no_of_tables]; // Number of auto-incremented columns
			int[] no_of_blob = new int[no_of_tables]; // Number of BLOB columns
			int[] no_of_intCols = new int[no_of_tables]; // Number of integer columns
			
			int i=0;
			/* Iterate over all tables to get data */
			for(String t : tableNames){
				rs = md.getColumns(null,null,t,null);
				int tmp1=0; // Number of columns in a table
				int tmp2=0; // Number of integer columns in a table
				int tmp3=0; // Number of auto-incremented columns in a table
				int tmp4=0; // Number of BLOB columns in a table
				int tmp5=0; // Number of indexes in a table
				int tmp6=0; // Number of foreign keys 
				while(rs.next()){
					tmp1++;
					String name = rs.getString(6); // returns typename of the column
					String incr = rs.getString(23); // returns a string: YES if column is auto-incremented, otherwise NO
					if(name.equalsIgnoreCase("INT") || name.equalsIgnoreCase("INTEGER"))tmp2++;
					if(name.equalsIgnoreCase("BLOB"))tmp4++;
					boolean b2 = incr.equalsIgnoreCase("YES");
					if(b2)tmp3++;
				}
				
				/* Since rows are not a part of metadata but actual data we need to run a query to count rows */
				Statement st = con.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_UPDATABLE);
				rs = st.executeQuery("SELECT COUNT(*) FROM " + t + ";");
				rs.next();
				no_of_rows[i] = rs.getInt(1);
				
				/* Find number of indexes for a table */
				rs = md.getIndexInfo(null,null,t,false,false); 
				while(rs.next()){
					tmp5++;
				}
				
				/* Find mumber of foreign keys */
				for(String t2 : tableNames){
					rs = md.getCrossReference(null,null,t2,null,null,t);
					while(rs.next())tmp6++;
				}
				
				/* Storing data in ith element of all arrays */
				no_of_cols[i] = tmp1;
				no_of_intCols[i] = tmp2;
				no_of_autoInc[i] = tmp3;
				no_of_blob[i] = tmp4;
				no_of_index[i] = tmp5;
				no_of_fk[i] = tmp6;
				i++;
			}
			/* Printing results to console */
			System.out.print("\n================================= INFORMATION FOR ");
			System.out.println( dataBaseName + " DATABASE ================================");
			System.out.format("%-75s : " , "Total number of tables ");
			System.out.println(no_of_tables);
			System.out.format("%-75s : " , "Min, Max, and Average number of columns per table");
			printAvgMinMaxStdDev(no_of_cols);
			System.out.format("%-75s : " , "Min, Max, and Average number of rows present per table");
			printAvgMinMaxStdDev(no_of_rows);
			System.out.format("%-75s : " , "Min, Max, and Average number of FKs present per table");
			printAvgMinMaxStdDev(no_of_fk);
			System.out.format("%-75s : " , "Min, Max, and Average number of indexes present per table");
			printAvgMinMaxStdDev(no_of_index);
			System.out.format("%-75s : " , "Min, Max, and Average number of auto incremented columns present per table");
			printAvgMinMaxStdDev(no_of_autoInc);
			System.out.format("%-75s : " , "Min, Max, and Average number of BLOB columns present per table");
			printAvgMinMaxStdDev(no_of_blob);
			System.out.format("%-75s : " , "Min, Max, and Average number of INTEGER columns present per table");
			printAvgMinMaxStdDev(no_of_intCols);
		}catch(SQLException e){
			e.printStackTrace();
		}
	}
	
	private static void printAvgMinMaxStdDev(int[] ar){
		float size = ar.length ;
    	if(size<=0)return;
    	int min = ar[0] , min_index=0;
    	int max = ar[0] , max_index=0;
    	float sum = ar[0];
    	/* Sum, Min and Max */
    	for(int i=1 ; i<size ; i++){
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
    	System.out.println(min + ", " + max + ", " + avg); 
    }
}
