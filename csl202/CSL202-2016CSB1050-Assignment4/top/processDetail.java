package top;
import java.io.*;
import java.sql.*;
import java.util.*;
import java.io.Console;
import java.util.regex.*;
import javax.mail.*;
import javax.mail.internet.*;
import javax.activation.*;
import java.util.Properties;
import java.util.Scanner;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.text.SimpleDateFormat;
import java.util.Date;

public class processDetail{
	public int PID;
	public String user;
	public float CPU;
	public float MEM;
	public String command;
	public int cpu_violation_time;
	public int mem_violation_time;
	public String TIME;
	public void setPID(int a1){
		PID = a1;
	}
	public void setUser_COMM_TIME(String a1 , String a2 , String a3){
		user = a1;
		command = a2;
		TIME = a3;
	}
	public void setCPU_MEM(float f1 , float f2){
		CPU = f1;
		MEM = f2;
	}
	public void setVTC(int a1){
		cpu_violation_time = a1;
	}
	public void setVTM(int a1){
		mem_violation_time = a1;
	}
	public String print(){
		String output = "";
		output += String.valueOf(PID);
		output += "\t";
		output += user;
		output += "\t";
		output += String.valueOf(CPU);
		output += "\t";
		output += String.valueOf(MEM);
		output += "\t";
		output += TIME;
		output += "\t";
		output += command;
		return output;
	}
}
