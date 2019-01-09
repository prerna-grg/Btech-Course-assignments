import java.util.Random;

public class RandomContact {

	private static String Con = "9";
	
    public String getCon() {
		Con = "9";
		for(int i=0 ; i<9 ; i++){	
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(10) + '0');
			Con += c;
		}
		return Con;
		
    }

}


