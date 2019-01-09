/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package javaapplication1;

/**
 *
 * @author prerna
 */


import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.GregorianCalendar;
import java.util.Random;

public class RandomData {

	private static java.util.Date utilDate = null;
	private static String P =  "1";
	private static String Con = "9";
	private static String Mail = "";
	
    public java.util.Date getDate(int start , int end) {

		GregorianCalendar gc = new GregorianCalendar();
		int year = randBetween(start, end);
		gc.set(GregorianCalendar.YEAR, year);
		int dayOfYear = randBetween(1, gc.getActualMaximum(GregorianCalendar.DAY_OF_YEAR));
		gc.set(GregorianCalendar.DAY_OF_YEAR, dayOfYear);
		String date = gc.get(GregorianCalendar.YEAR) + "/" + (gc.get(GregorianCalendar.MONTH) + 1) + "/" + gc.get(GregorianCalendar.DAY_OF_MONTH);
		try {
			SimpleDateFormat formatter = new SimpleDateFormat("yyyy/MM/dd");
			utilDate = formatter.parse(date);
		} catch (ParseException e) {
			System.out.println(e.toString());
		}
		return utilDate;
    }

    public static int randBetween(int start, int end) {
        return start + (int)Math.round(Math.random() * (end - start));
    }

    public String getPost() {
		P = "1";
		for(int i=0 ; i<5 ; i++){	
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(10) + '0');
			P += c;
		}
		return P;
    }
	
    public String getMob() {
		Con = "9";
		for(int i=0 ; i<9 ; i++){	
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(10) + '0');
			Con += c;
		}
		return Con;
    }

	public String getMail(){
		Mail = "";
		for(int i=0; i<5 ; i++){
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(26) + 'a');
			Mail += c;
		}
		Mail += "@gmail.com" ;
		return Mail;
	}
}

