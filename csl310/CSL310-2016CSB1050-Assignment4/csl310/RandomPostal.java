import java.util.Random;

public class RandomPostal{

	private static String P =  "1";
	
    public String getPost() {
		P = "1";
		for(int i=0 ; i<5 ; i++){	
			Random rnd = new Random();
			char c = (char) (rnd.nextInt(10) + '0');
			P += c;
		}
		return P;
    }

}


