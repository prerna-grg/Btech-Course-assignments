package algorithms;
public class BubbleSort extends SortingAlgorithms{
	//@override
	public void print(){   
		System.out.println("Instantiated Bubble Sort");
	}
	//Sorting algorithm
	public int[] sort(int[] arr){
        int n = arr.length;
        //traverse through the array
        for (int i = 0; i < n-1; i++){
            for (int j = 0; j < n-i-1; j++){
                if (arr[j] > arr[j+1]){
                	//swap elements
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }
			}
		}
		return arr;
	}
}

