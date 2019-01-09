package algorithms;
import java.lang.Math;

public class  JumpSearch extends SearchAlgorithms{  
	//@override
	public void print(){   
		System.out.println("Instantiated Jump Search");
	}
	// jump search algorithm
	public void search(int[] arr , int x){
		//starting time of the algorithm
		long startTime = System.nanoTime();
		int n = arr.length;
		int result = jumpSearch(arr, x );
		long endTime = System.nanoTime();
		//ending time of the algorithm
		
		//if element is not found the value of result is -1
		if(result==-1)System.out.println("Element is not present in array");
		else System.out.println("Element is present at index: " + result );
		System.out.println("Time taken through Jump Search: " + (endTime - startTime) + " ns" );
	}
	
	//The following function is private to this class and is used to search
	public static int jumpSearch(int[] arr, int x){
        int n = arr.length; //length of array
        int step = (int)Math.floor(Math.sqrt(n));
        int prev = 0;
        while (arr[Math.min(step, n)-1] < x){
            prev = step;
            step += (int)Math.floor(Math.sqrt(n));
            if (prev >= n) return -1;
        }
        while (arr[prev] < x){
            prev++;
            if (prev == Math.min(step, n)) return -1;
        }
        if (arr[prev] == x) return prev;
		return -1;
	}	
}

