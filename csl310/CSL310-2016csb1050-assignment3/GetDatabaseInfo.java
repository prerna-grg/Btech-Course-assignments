import java.sql.*;
import java.util.Properties;
import java.io.*;
import java.util.*;
import java.lang.Math;
import java.text.DecimalFormat;
import java.io.Console;

public class GetDatabaseInfo
{
	public static void main(String[] args) throws Exception {
	try{
	        // The JDBC Connector Class.
		Class.forName("com.mysql.jdbc.Driver");
		Console console = System.console();

		String USERNAME = console.readLine("Enter DB login: ");
		char[] PASSWORD = console.readPassword("Enter DB password: ");  // to read password with echoing disabled
		String pass = String.valueOf(PASSWORD);   // converting char[] to string

                Connection connection = DriverManager.getConnection(args[0],USERNAME,pass);  // connection object
		String DatabaseName = connection.getCatalog();   // gives the name of the database using the connection object
		System.out.println("=============================== INFORMATION FOR "+DatabaseName+" DATABASE ============================");
		DatabaseMetaData metadata = connection.getMetaData();   /* returns a DatabaseMetaData object that contains information about 
		the database to which connection is made */

		Statement st = connection.createStatement(); // creates a statement object which can be used to execute sql statements.
		String[] types = {"TABLE"}; // this program extracts information about tables only
		ResultSet resultSetTables = metadata.getTables(null, null, "%", types);   /* catalog and schemaPattern have been set to null.
		 % means matching any table name pattern */
		int tableCount =0;   // for counting total number of tables in database
		while (resultSetTables.next()) 
		{
		    tableCount++;
		}

		int[] tableColumns = new int[tableCount];           // to store number of columns in each table
		int[] blobColumns = new int[tableCount];            // to store number of columns having type as 'BLOB' in each table
		int[] integerColumns = new int[tableCount];         // to store number of columns having type as 'INTEGER' in each table
		int[] autoIncrementColumns = new int[tableCount];   // to store number of auto incremented columns in each table
		int[] totalRowsInTable = new int[tableCount];       // to store total number of rows in each table
		int[] FKColumns = new int[tableCount];              // to store number of foreign keys present in each table
		int[] IndexColumns = new int[tableCount];           // to store number of indexes present in each table

		ResultSet rs = metadata.getTables(null, null, "%", types);  // for iterating over each table
		int i=0;
		int totalColumns=0;                                 // stores the sum of all elements in tableColumns array
		int totalBlobColumns=0;                             // stores the sum of all elements in blobColumns array
		int totalIntegerColumns=0;                          // stores the sum of all elements in integerColumns array
		int totalAutoIncrementColumns=0;                    // stores the sum of all elements in autoIncrementColumns array
		int totalRows=0;                                    // stores the sum of all elements in totalRowsInTable array
		int totalFKColumns=0;                               // stores the sum of all elements in FKColumns array
		int totalIndexColumns=0;                            // stores the sum of all elements in IndexColumns array

		while(rs.next())
		{
                        String tableName = rs.getString(3);       // each table description of result set has third column equal to TABLE_NAME
                        ResultSet numRows = st.executeQuery("SELECT COUNT(*) FROM "+ tableName);  /* create a sql statement to count number of
                        row in each table */ 
                        while(numRows.next())
                        {
                           totalRowsInTable[i] = numRows.getInt(1);  // get number of rows in a table
                           totalRows += totalRowsInTable[i];
                        }
                        ResultSet resultSetFK = metadata.getExportedKeys(null, null, tableName); // to get metadata of foreign keys
                        while (resultSetFK.next()) {
                           FKColumns[i]++;
                           totalFKColumns++;
                        }

                        ResultSet resultSetIndex = metadata.getIndexInfo(null, null, tableName, false, false); // to get metadata of indexes
                        while (resultSetIndex.next()) {
                           IndexColumns[i]++;
                           totalIndexColumns++;
                        }
                        ResultSet resultSetColumns = metadata.getColumns(null, null, tableName, null); // to get metadata of columns of a table
                        
                        while (resultSetColumns.next()) {
                                String dbColumnTypeName = resultSetColumns.getString(6);     // get the type of column
                                if(dbColumnTypeName.equalsIgnoreCase("BLOB")) {    // if it is blob then increment blobColumns[i]
                                   blobColumns[i]++;
                                   totalBlobColumns++;
                                }

                                if(dbColumnTypeName.equalsIgnoreCase("INTEGER") || dbColumnTypeName.equalsIgnoreCase("INT")) {
                                   integerColumns[i]++;
                                   totalIntegerColumns++; 
                                }

                                String is_autoIncrement = resultSetColumns.getString("IS_AUTOINCREMENT");// check if column is auto_incremented
                                if(is_autoIncrement.equals("YES")) {
                                   autoIncrementColumns[i]++;
                                   totalAutoIncrementColumns++;
                                }
                                
                                tableColumns[i]++;
                                totalColumns++;

                        }
                        i++;
		}
		Arrays.sort(tableColumns);                 // to compute min and max
		double averageColumns = (double)totalColumns/tableCount;
		Arrays.sort(autoIncrementColumns);
		double averageAutoIncrementColumns = (double)totalAutoIncrementColumns/tableCount;
		Arrays.sort(blobColumns);
		double averageBlobColumns = (double)totalBlobColumns/tableCount;
		Arrays.sort(integerColumns);
		double averageIntegerColumns = (double)totalIntegerColumns/tableCount;
		Arrays.sort(totalRowsInTable);
		double averageRows = (double)totalRows/tableCount;
		Arrays.sort(FKColumns);
		double averageFKColumns = (double)totalFKColumns/tableCount;
		Arrays.sort(IndexColumns);
		double averageIndexColumns = (double)totalIndexColumns/tableCount; 

		DecimalFormat df = new DecimalFormat("#0.0");    // to print a single digit after decimal
		DecimalFormat df2 = new DecimalFormat("#0.00");  // to print two digits after decimal

		System.out.format("%-75s%-3s","Total number of tables" ," : ");   // formatted output
		System.out.println( tableCount);
		System.out.format("%-75s%-3s","Min, Max, and Average number of columns per table" ," : ");
		System.out.println( tableColumns[0]+", "+tableColumns[tableColumns.length-1]+", "+ df.format(averageColumns));
		System.out.format("%-75s%-3s","Min, Max, and Average number of rows present per table" ," : ");
		System.out.println( totalRowsInTable[0]+", "+totalRowsInTable[totalRowsInTable.length-1]+", "+ df.format(averageRows));
		System.out.format("%-75s%-3s","Min, Max, and Average number of FKs present per table" ," : ");
		System.out.println( FKColumns[0]+", "+FKColumns[FKColumns.length-1]+", "+ df.format(averageFKColumns));
		System.out.format("%-75s%-3s","Min, Max, and Average number of indexes present per table" ," : ");
		System.out.println( IndexColumns[0]+", "+IndexColumns[IndexColumns.length-1]+", "+ df.format(averageIndexColumns));
		System.out.format("%-75s%-3s","Min, Max, and Average number of auto incremented columns present per table" ," : ");
		System.out.println(autoIncrementColumns[0]+", "+autoIncrementColumns[autoIncrementColumns.length-1]+", "+ df.format(averageAutoIncrementColumns));
		System.out.format("%-75s%-3s","Min, Max, and Average number of BLOB columns present per table" ," : ");
		System.out.println(blobColumns[0]+", "+blobColumns[blobColumns.length-1]+", "+ df2.format(averageBlobColumns));
		System.out.format("%-75s%-3s","Min, Max, and Average number of INTEGER columns present per table" ," : ");
		System.out.println(integerColumns[0]+", "+integerColumns[integerColumns.length-1]+", "+ df2.format(averageIntegerColumns));

		connection.close();  
	}
	catch(SQLException s){
		System.out.println("Statement cannot be executed");}

	}
}


