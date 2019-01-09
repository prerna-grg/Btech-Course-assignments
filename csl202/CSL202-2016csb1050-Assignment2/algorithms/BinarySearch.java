package algorithms;
public class BinarySearch extends SearchAlgorithms{  
	//@override 
	public void print(){   
		System.out.println("Instantiated Binary Search");
	}
	// binary search algorithm
	public void search(int[] arr , int x){
		//starting time of the algorithm
		long startTime = System.nanoTime();
		int n = arr.length;
		int result = binarySearch(arr, 0 , n-1, x);
		long endTime = System.nanoTime();
		//starting time of the algorithm
		
		//if element is not found the value of result is -1
		if(result==-1)System.out.println("Element is not present in array");
		else System.out.println("Element is present at index: " + result );
		System.out.println("Time taken through Binary Search : " + (endTime - startTime) + " ns" );
	}
	//The following function is private to this class and is used to search
	private static int binarySearch(int arr[], int first, int last, int key){  
	   int mid = (first + last)/2;  
	   while( first <= last ){  
		  if ( arr[mid] < key ){  
		    first = mid + 1;     
		  }else if ( arr[mid] == key ){  
		    return mid;
		  }else{  
		     last = mid - 1;  
		  }  
		  mid = (first + last)/2;  
	   }  
	   return -1;  
	}
}


