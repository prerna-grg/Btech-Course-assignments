/**
 * Contains the utility methods used by various parts of this application.
 */
package engine;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * @author Balwinder Sodhi
 */
public class Utils {

	/**
	 * Date format to be used for printing log messages on console.
	 */
	private static SimpleDateFormat df = new SimpleDateFormat("dd-MM-yyyy, HH:mm:ss.SSS");
	/**
	 * Returns the current date and time in the format dd-MM-yyyy, HH:mm:ss.SSS
	 * @return Current date and time in "dd-MM-yyyy, HH:mm:ss.SSS" format.
	 */
	public static String currentTime() {
		return df.format(new Date());
	}
}
