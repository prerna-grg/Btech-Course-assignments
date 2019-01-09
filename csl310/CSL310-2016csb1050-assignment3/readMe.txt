RUN INSTRUCTIONS:

$ javac getDatabaseMetaData.java
$ java -cp ./mysql-connector.jar:. getDatabaseMetaData mysql-link-to-database


EXPLANATION:
The “java.sql.DatabaseMetaData” and related API has been used to retrieve the useful information about a database.
The information extracted is as follows:

To create connection I have used Java's Connection object

To get the metadata I have used these classes and respective functions:
1) DatabaseMetaData -- getMetaData()
2) ResultSet -- getTables(String catalog,String schemaPattern,String tableNamePattern,String[] types)
3) Statement -- createStatement()
4) getIndexInfo(String catalog,String schema,String table,boolean unique,boolean approximate)
5) getCrossReference(String parentCatalog,String parentSchema,String parentTable,String foreignCatalog,String foreignSchema,String foreignTable)

After extracting the data, it is printed as output to console in a formatted manner as shown in sample run


SAMPLE RUN AND OUTPUTS:

prerna@prerna-pc:~/CSL310-2016csb1050-assignment3$ javac getDatabaseMetaData.java 
prerna@prerna-pc:~/CSL310-2016csb1050-assignment3$ java -cp ./mysql-connector.jar:. getDatabaseMetaData jdbc:mysql://localhost:3306/sakila

Enter DB login: root
Enter DB password: 

================================= INFORMATION FOR sakila DATABASE ================================
Total number of tables                                                      : 16
Min, Max, and Average number of columns per table                           : 3, 13, 5.625
Min, Max, and Average number of rows present per table                      : 2, 16049, 2954.5625
Min, Max, and Average number of FKs present per table                       : 0, 3, 1.375
Min, Max, and Average number of indexes present per table                   : 1, 7, 3.0
Min, Max, and Average number of auto incremented columns present per table  : 0, 1, 0.8125
Min, Max, and Average number of BLOB columns present per table              : 0, 1, 0.0625
Min, Max, and Average number of INTEGER columns present per table           : 0, 1, 0.125
