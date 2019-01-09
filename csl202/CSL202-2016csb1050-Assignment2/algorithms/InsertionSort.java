package algorithms;
public class InsertionSort extends SortingAlgorithms{  
	//@override
	public void print(){   
		System.out.println("Instantiated Insertion Sort");
	}
	public int[] sort(int[] arr){
		int n = arr.length;
		int i, key, j;
		//traverse through the array
		for (i = 1; i < n; i++){
			key = arr[i];
			j = i-1;
			//shift the elements
			while (j >= 0 && arr[j] > key){
				arr[j+1] = arr[j];
				j = j-1;
			}
			arr[j+1] = key;
		}
		return arr;
	}
}
