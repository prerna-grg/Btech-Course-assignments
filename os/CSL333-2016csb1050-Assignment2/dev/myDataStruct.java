package dev;
import java.util.*;

public class myDataStruct extends Exception{

	public static HashMap<Long , Integer> M = new HashMap<Long , Integer>();
	public static Deque<Long> Q = new LinkedList<>();
	
	public myDataStruct(){
		Q.add((long)2);
		M.put((long)2,1);
	}
	
	public static void recordGeneratedNumber(long number){
		if ( M.containsKey(number) ){
			return;
		}else{
			M.put(number,1);
			Q.addLast(number);
		}
	}
	
	public static long takeOldestGeneratedNumber(){
		long num = Q.peek();
		try{
			Q.removeFirst();
		}catch(NoSuchElementException ne ){
			System.out.println("No more numbers found");
		}finally{
			return num ;
		}
	}
	
	public static long length(){
		return M.size();
	}
	
	public static long Qsize(){
		return Q.size();
	}
	
	public static long printLast(){
		return Q.peekLast();
	}
	
	public static void printAll(){
		for (Map.Entry<Long,Integer> entry : M.entrySet()){
            System.out.print( entry.getKey() + " " );
        }
        System.out.println();
	}
	
}
