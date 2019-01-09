package algorithms;

/*
	This java file is a factory used to access sorting and search algorithms.
	The selection is based on string matching.
	Any additional algorithm being added should be reflected here in this similar manner
*/
public class GetAlgorithmFactory{  
      
   //use getAlgo method to get object of type Algo   
	public SortingAlgorithms getSortAlgo(String Algo){  
		if(Algo == null){  
			return null;  
		}  
		if(Algo.equalsIgnoreCase("bubble")) {  
			return new BubbleSort();  
		}   
		else if(Algo.equalsIgnoreCase("insertion")){  
			return new InsertionSort();  
		}   
		else if(Algo.equalsIgnoreCase("selection")) {  
			return new SelectionSort();  
		}
      	return null;
	}
	public SearchAlgorithms getSearchAlgo(String Algo){
		if(Algo == null){  
			return null;  
		}  
		if(Algo.equalsIgnoreCase("linear")) {  
			return new LinearSearch();  
		}   
		else if(Algo.equalsIgnoreCase("binary")){  
			return new BinarySearch();  
		}   
		else if(Algo.equalsIgnoreCase("jump")) {  
			return new JumpSearch();  
		}
      	return null;
	}
}
