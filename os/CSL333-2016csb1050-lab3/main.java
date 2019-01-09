import java.util.Random;
import java.util.Arrays;

public class main {

	// set the given parameters 
	public static int range = 5000 ;
	public static int size = 1000 ;
		
	/************************************* SSTF scheduling ******************************************/
	public static void _SSTF_( int num[] , int head ){
		
		boolean acc[] = new boolean[size];
		for (int i = 0; i < size; i++){
			// initialise serviced state to false for all
		    acc[i] = false;
		}
		int sstf_count = 0;
		for (int i = 0; i < size; i++){
			int min_d = Integer.MAX_VALUE ; // initialisation
			int min_i = -1; // initialisation
			// Find minimum seek distance
			for (int j = 0; j < size; j++){
				if ( acc[j] == false ){
					int temp = Math.abs(num[j] - head) ;
					if ( temp < min_d ){
						min_i = j ;
						min_d = temp ;
					}
				}
			}
			// move the head and add the distance to total count
			sstf_count += Math.abs(num[min_i] - head) ;
			head = num[min_i] ;
			
			// change the serviced state to true
			acc[min_i] = true; 
		}
		System.out.println("Total Movements using SSTF scheduling: " + sstf_count);
	}
	
	/************************************* C-SCAN scheduling ******************************************/
	public static void _CSCAN_( int num[] , int head ){
		
		int cscan_count = range - 1 - head; // go upto the right end first and process all coming in the way
		if ( num[0] >= head ){
			cscan_count -= range - 1 - num[size-1] ; // if any was left over go to the left
		}else{
			// go right till all are done
			cscan_count += range-1 ;
			int i=0;
			for (i = 0; i < size; i++){
				if ( num[i] < head ) continue;
				else break ;
			}
			// increment the distance
			cscan_count += num[i-1];
		}
		System.out.println("Total Movements using C-SCAN scheduling: " + cscan_count);
	}
	
	/************************************* C-LOOK scheduling ******************************************/
	public static void _CLOOK_(int num[] , int head ){
		int clook_count = 0;
		if ( num[size-1] >= head ){
			clook_count += num[size-1] - head ; // go right if you need to
		}else{
			clook_count += head - num[size-1] ;
		}
		
		// go left if any was left while going right
		if ( num[0] < head ){
			clook_count += num[size-1] - num[0] ; 
			int i=0;
			for (i = 0; i < size; i++){
				if ( num[i] < head ) continue;
				else break ;
			}
			// increment the distance
			clook_count += num[i-1] - num[0] ;
		}
		System.out.println("Total Movements using C_LOOK scheduling: " + clook_count);
	}	
	

	public static void main(String args[]){
		
		if(args.length != 1){
			System.out.println("Invalid Usage\njava main <head>");
			return;
		}
		
		// read the head as a command line parameter
		int head = Integer.parseInt(args[0]);
		if ( head < 0 || head >= range ){
			System.out.println("Invalid head value, Allowed position : (0-" + (range-1) + ")" );
		}
		
		// create the array 
		Random random = new Random();
		int num[] = new int[size];
		
		for (int i = 0; i < size; i++){
			// generate random disk cylinder requests
		    num[i] = random.nextInt(range);
		}
		
		head = Integer.parseInt(args[0]);
		if ( head < 0 || head >= range ){
			System.out.println("Invalid head value, Allowed position : (0-" + (range-1) + ")" );
			return;
		}
		
		// Call SSTF
		_SSTF_( num , head ) ;
		Arrays.sort(num); // sort the input array

		// Call CSCAN
		_CSCAN_(num , head);
		
		// Call CLOOK
		_CLOOK_(num, head);
		
	}
}
