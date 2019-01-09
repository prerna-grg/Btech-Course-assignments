//package csl310.db;

public class AccountHolder {
    public Integer id;
    public String PAN;
    public String First_Name;
    public String Last_Name;

    @Override
    public String toString() {
        return "AccountHolder{" + "id=" + id + ", PAN=" + PAN + ", First_Name=" + First_Name + ", Last_Name=" + Last_Name +"}";
    }
}
