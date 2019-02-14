import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.*; 
import java.util.*; 
import java.util.HashMap; 
import java.util.Map; 

public class DeadlockDetect {
	
	public static void main (String args[]){
	
		if ( args.length != 1){
			System.out.println( "Invalid Usage");
			System.out.println("Use: java DeadlockDetect filename.csv");
			return ;
		}
		File f1 = new File(args[0]);
		if(!f1.exists()){
			System.out.println( "Error: File named \"" + args[0] + "\" does not exist");
			return;
		}
		BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        int Rn = 0 ; // number of resources
        int Pn = 0;
        try {
        	// read the csv file to get the initialisation data dimensions
            br = new BufferedReader(new FileReader(args[0]));
            if ((line = br.readLine()) != null) {
                String[] data = line.split(cvsSplitBy);
                Rn = data.length/3 ; // number of resources
				Pn++; // number of processes
            }
            while((line = br.readLine()) != null){
            	Pn++;
            }
            // allocate the required matrices
            int P[][] = new int[Pn][Rn] ; // allocation matrix
            int Q[][] = new int[Pn][Rn] ; // requested matrix
            int W[] = new int[Rn] ; // available matrix
            br = new BufferedReader(new FileReader(args[0]));
            int i = 0 ;
            // fill the matrices using data from file
            while ((line = br.readLine()) != null) {
            	String[] data = line.split(cvsSplitBy);
            	int k=0;
            	for ( k=0 ; k<Rn ; k++){
            		P[i][k] = Integer.parseInt(data[k]);
            	}
            	for ( k=Rn ; k<2*Rn ; k++){
            		Q[i][k-Rn] = Integer.parseInt(data[k]);
            	}
            	if(i==0){
            		for ( k=2*Rn ; k<3*Rn ; k++){
            			W[k-2*Rn] = Integer.parseInt(data[k]);
            		}
            	}
            	i++;
            }
            
            // marker array .. initialised with all false.
            boolean marks[] = new boolean[Pn];
            for ( int j=0 ; j<Pn ; j++){
            	marks[j] = false;
            }
            
            // Marks the processes that can complete without going into deadlock
            // After this loop completes if any process is unmarked then it is in deadlock
            while ( true ){
            	boolean read = false;
		        for ( i=0 ; i<Pn ; i++){
		        	if( marks[i]==false){
		        		int count = 0;
				    	for ( int j=0 ; j<Rn ; j++){
				    		if ( Q[i][j] <= W[j] ){
				    			count++;
				    		}
				    	}
				    	if ( count == Rn ){
				    		// all resources are available
				    		marks[i] = true;
				    		read = true ;
				    		for ( int j=0 ; j<Rn ; j++){
				    			W[j] += P[i][j] ; // finish the process and return all the allocated resources
				    		}
				    	}
				    }
		        }
		        if ( read==false )break; // no more processes can complete
			}
			
			ArrayList<String> Pro = new ArrayList<String>(); // processes in deadlock
			HashMap<String, Integer> Res = new HashMap<>(); // resources causing deadlock
			
			// check the data and fill the values
			for ( i=0 ; i<Pn ; i++){
            	if( marks[i]==false){
            		Pro.add("P" + (i+1));
		        	for ( int j=0 ; j<Rn ; j++){
		        		if ( Q[i][j] > W[j] ){
				    		Res.put("R" + (j+1) , 1);
				    	}
		        	}
		        }
		    }
		    // Printing the results to console
		    System.out.println("Using input from " + args[0] );
		    if ( Pro.size()!=0 ){
			    System.out.print("System state: Deadlocked. Processes: ");
			    for( int y=0 ; y<Pro.size()-1 ; y++ ){
			    	System.out.print(Pro.get(y) + ", " );
			    }
			    System.out.print(Pro.get(Pro.size()-1) + ". Resources: " );
			    int f = 0;
			    for (Map.Entry<String,Integer> entry : Res.entrySet()){
			    	f++;
			    	System.out.print(entry.getKey());
			    	if ( Res.size() == f ){
			    		System.out.print(".");
			    	}else{
			    		System.out.print(", ");
			    	}
			    }
			    System.out.print("\n" );
			}else{
				System.out.println("System state: No Deadlocks ");
			}
		    
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
	}
}
