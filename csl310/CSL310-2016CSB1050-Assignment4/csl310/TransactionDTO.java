//package csl310.db;
import java.sql.Date;

public class TransactionDTO {
    public Integer TransactionID;
    public String TransactionType;
    public Date TransactionDatetime;
    public Integer Amount ;
    public Integer AccountID;
    public String Category;
    public String Remarks;
    
    @Override
    public String toString() {
        return "ID: " + TransactionID + " Type: " + TransactionType + " Date: " + TransactionDatetime + " Amount: " + Amount + " Account: " + AccountID + " Category: " + Category + " Remarks: " + Remarks;
    }
}
