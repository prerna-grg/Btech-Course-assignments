import dev.*;
import java.util.concurrent.TimeUnit ;
import java.util.*;

/* Data Structure to hold the unique numbers generated */
class myDataStruct{
	public HashMap<Long , Integer> M = new HashMap<Long , Integer>();
	public Deque<Long> Q = new ArrayDeque<>();
	public Deque<Long> PQ = new ArrayDeque<>();
}


/* Thread class to allow threads to run repeatedly by picking up the available base and pushing the corresponding numbers */
class MyThread implements Runnable{

	/* Thread Initialisation */
	Thread t ;
	boolean type ;
	int c ; 
	int b ; 
	MyThread ( boolean t_id , int n1 , int n2 ){
		t = new Thread(this) ;
		type = t_id;
		c = n1 ;
		b = n2 ;
	}
	
	/* Run methods : picks up a base , calculates the numbers , sees it's turn , pushes the numbers and moves to next */
	@Override
	public void run(){
		long nxtNumber = -1;
		int endLoop = Device.MULTIPLIERS.length; /* number of prime multipliers */
		Device dev = null;
		/* Real or unreal is given as argument in constructor */
		if ( type == true){
			RealDevice.DeviceConfig dc = new RealDevice.DeviceConfig(c, b, 1);
			dev = new RealDevice(dc);
		}else{
			dev = new UnrealDevice(1);
		}
		/* Until you get desired numbers keep calculating */
		while (!getNthNum.done) {
			if ( getNthNum.uniqueNumGenerated.M.size() >= getNthNum.n) {
				getNthNum.done = true;
				break;
			}
			
			long base = 0;
			/* Get the next base */
			while( !getNthNum.done){
				synchronized(getNthNum.uniqueNumGenerated){
					if( getNthNum.uniqueNumGenerated.Q.size() != 0){
						base = getNthNum.uniqueNumGenerated.Q.peek(); // get the next base from the queue
						getNthNum.uniqueNumGenerated.PQ.add(base); // push to priority queue
						getNthNum.uniqueNumGenerated.Q.removeFirst(); // remove from the queue
						break;
					}
				}
			}
			
			/* Generate the new numbers from the multipliers */
			long ar[] = new long[endLoop] ;
			for (int i = 0; i < endLoop; i++) {
				try{
					nxtNumber = dev.f(base, i);
					getNthNum.count++;
					ar[i] = nxtNumber;
				}catch(Exception e){
					//System.out.println("Work Done .. thread interrupted");
				}
			}
				
			/* wait for your turn and push the numbers to set */
			while( !getNthNum.done){
				synchronized(getNthNum.uniqueNumGenerated) {
					if ( base == getNthNum.uniqueNumGenerated.PQ.peek() ){
						getNthNum.uniqueNumGenerated.PQ.removeFirst();
						for ( long me : ar ){
							if ( getNthNum.uniqueNumGenerated.M.size() >= getNthNum.n ){
								getNthNum.done = true; // if desired size reached stop :)
								break;
							}
							else if ( getNthNum.uniqueNumGenerated.M.containsKey(me) ){
								continue; // already exists
							}else{
								getNthNum.uniqueNumGenerated.Q.addLast(me); // push to queue
								getNthNum.uniqueNumGenerated.M.put(me,getNthNum.uniqueNumGenerated.M.size()+1); // put in set
							}
						}
						getNthNum.uniqueNumGenerated.notifyAll(); // notify others that the struct is available now
						break;
					}else{
						try{
							getNthNum.uniqueNumGenerated.wait(); // wait for the struct to be free
						}catch(Exception e){
							//System.out.println("Work done .. thread interrupted");
						}
					}
				}
			}
		}
		return;
	}
}

public class getNthNum{

	public static myDataStruct uniqueNumGenerated = new myDataStruct(); // instance of data structure ( queue , priority queue , set )
	public static boolean done = false; // status of set size
	public static long n = 0; // desired size (user input)
	public static String type = "real" ; // device type default
	public static int count = 0; // device invoked
	public static void main(String args[]){
		uniqueNumGenerated.Q.add(Long.valueOf(2));
		uniqueNumGenerated.M.put(Long.valueOf(2),1);
		if ( args.length < 3){
			System.out.println("Invalid Usage");
			return;
		}
		
		System.out.println("----------------------------------------");
		System.out.println("RESULTS SUMMARY");
		System.out.println("----------------------------------------");

		
		// desired size
		n = Long.parseLong(args[0]);
		System.out.println(String.format("%-"+29+"s", "Target Count (n)" ).replaceAll("\\s(?=\\s+$|$)", ".")+": " + n );
		int t = Integer.parseInt(args[1]);
		System.out.println(String.format("%-"+29+"s", "Number of threads" ).replaceAll("\\s(?=\\s+$|$)", ".")+": " + t );
		type = args[2];
		
		// get the device type 
		boolean t_id = true;
		if(!type.equalsIgnoreCase("real")){
			t_id = false;
		}
		System.out.println(String.format("%-"+29+"s", "Used real device" ).replaceAll("\\s(?=\\s+$|$)", ".")+": " +  t_id );
		// compute delay
		int c_delay = 3 ;
		if ( args.length >= 4 ){
			c_delay = Integer.parseInt(args[3]);
		}
		// boot delay
		int b_delay = 250 ;
		if ( args.length >= 5 ){
			b_delay = Integer.parseInt(args[4]);
		}
		
		// initialise the threads
		MyThread threads[] = new MyThread[t];
		Thread thr[] = new Thread[t];
		
		// start the timer
		long start = System.currentTimeMillis() ;
		for (int i=0 ; i<t ; i++){
			threads[i] = new MyThread(t_id , c_delay , b_delay);
			thr[i] = new Thread(threads[i]);
			thr[i].start();
		}
		
		for (int i=0 ; i<t ; i++){
			try{
				thr[i].join();
				if(uniqueNumGenerated.M.size()==n){
					break;
				}
				//System.out.println("--> " +  i);
			}catch(Exception e){
				System.out.println("Exception in joining");
			}
		}
		// end the timer and print the results
		System.out.println(String.format("%-"+29+"s", "Time taken" ).replaceAll("\\s(?=\\s+$|$)", ".")+": " + (System.currentTimeMillis() - start)/1000.0 + " sec" );
		System.out.print(String.format("%-"+29+"s", "Resulting number" ).replaceAll("\\s(?=\\s+$|$)", ".")+": ");
		for (Map.Entry<Long,Integer> entry : uniqueNumGenerated.M.entrySet()){
			if( entry.getValue() == n ){
				System.out.print(entry.getKey());
				break;
			}
		}
		System.out.println();
		System.out.println(String.format("%-"+29+"s", "Device Invoked (approx)" ).replaceAll("\\s(?=\\s+$|$)", ".")+": " + count + " time");
		for (int i=0 ; i<t ; i++){
			thr[i].interrupt();
		}
	}
}
