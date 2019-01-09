package algorithms;
public class  LinearSearch extends SearchAlgorithms{  
	//@override  
	public void print(){   
		System.out.println("Instantiated Linear Search");
	}
	public void search(int[] arr , int x){
		//starting time of the algorithm
		long startTime = System.nanoTime();
		int n = arr.length;
		int i;
		int result = -1;
		//traversal through the array
		for(i=0; i<n; i++){
			if(arr[i] == x){
				result = i;
				break;
			}
		}
		long endTime = System.nanoTime();
		//ending time of the algorithm
		if(result==-1)System.out.println("Element is not present in array");
		else System.out.println("Element is present at index: " + result );
		System.out.println("Time taken through Linear Search : " + (endTime - startTime) + " ns" );
	}
	
}
