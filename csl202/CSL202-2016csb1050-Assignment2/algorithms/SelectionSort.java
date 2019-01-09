package algorithms;
public class SelectionSort extends SortingAlgorithms{  
	//@override  
	public void print(){   
		System.out.println("Instantiated Selection Sort");
	}
	public int[] sort(int[] arr){
		int n = arr.length;
		//Traverse through the array
		for (int i = 0; i < n-1; i++){
			int min_idx = i;
			for (int j = i+1; j < n; j++){
				if (arr[j] < arr[min_idx]) min_idx = j;
			}
			int temp = arr[min_idx];
			arr[min_idx] = arr[i];
			arr[i] = temp;
		}
		return arr;
	}
	
}
