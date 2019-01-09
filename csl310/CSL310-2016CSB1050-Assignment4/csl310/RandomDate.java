import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.GregorianCalendar;

public class RandomDate {

	private static java.util.Date utilDate = null;
	
    public java.util.Date getDate(int start , int end) {

		GregorianCalendar gc = new GregorianCalendar();
		int year = randBetween(start, end);
		gc.set(gc.YEAR, year);
		int dayOfYear = randBetween(1, gc.getActualMaximum(gc.DAY_OF_YEAR));
		gc.set(gc.DAY_OF_YEAR, dayOfYear);
		String date = gc.get(gc.YEAR) + "/" + (gc.get(gc.MONTH) + 1) + "/" + gc.get(gc.DAY_OF_MONTH);
		try {
			SimpleDateFormat formatter = new SimpleDateFormat("yyyy/MM/dd");
			utilDate = formatter.parse(date);
		} catch (ParseException e) {
			System.out.println(e.toString());
			e.printStackTrace();
		}
		return utilDate;
    }

    public static int randBetween(int start, int end) {
        return start + (int)Math.round(Math.random() * (end - start));
    }
}


