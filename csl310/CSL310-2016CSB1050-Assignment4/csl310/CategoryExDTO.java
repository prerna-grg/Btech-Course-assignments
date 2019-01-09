//package csl310.db;

public class CategoryExDTO {
    public String Category;
    public Integer Expenditure;

    @Override
    public String toString() {
    	String output = String.format("%-10s: %-20s %-12s: %s" ,"Category", Category ,"Expenditure" ,Expenditure) ;
        return output;
    }
}
