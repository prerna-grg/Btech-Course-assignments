import java.util.Random;

public class RandomPAN {

	private static String PAN = "A";
	
    public String getPAN() {
		PAN = "A";
		for(int i=0 ; i<4 ; i++){	
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(26) + 'A');
			PAN += c;
		}
		return PAN;
		
    }

}


