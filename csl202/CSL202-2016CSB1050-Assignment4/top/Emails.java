package top;
import java.util.*;
import javax.mail.*;
import javax.mail.internet.*;

public class Emails {

    private static String USER_NAME = "prernapc234";  // GMail user name (just the part before "@gmail.com")
    private static String PASSWORD = "qwertyu@"; // GMail password

    public void sendEmails( HashMap<Integer,processDetail> violators , ArrayList<String> emailIDs) {
		String host = "smtp.gmail.com"; // host name
		String port = "587"; // port name
        String from = USER_NAME; // sender
        String pass = PASSWORD;
        String subject = "Excess Resources Being Used on your system"; // subject of the email
        
        // setting up the desired properties
        Properties props = System.getProperties();
        props.put("mail.smtp.starttls.enable", "true");
        props.put("mail.smtp.host", host);
        props.put("mail.smtp.user", from);
        props.put("mail.smtp.password", pass);
        props.put("mail.smtp.port", port);
        props.put("mail.smtp.auth", "true");
		props.put("mail.smtp.ssl.trust", "smtp.gmail.com");

        Session session = Session.getDefaultInstance(props);
        MimeMessage message = new MimeMessage(session);

        try {
            message.setFrom(new InternetAddress(from));
            InternetAddress[] toAddress = new InternetAddress[emailIDs.size()];
			String body = "";
			int i=1;
			// loop over all the processes that violated
			for (Integer ID : violators.keySet()){
				processDetail temp = violators.get(ID);
           		body += "Violating Process: " + String.valueOf(i) ;
				body += "PID: " + String.valueOf(temp.PID) + "\n";
				body += "User: " + String.valueOf(temp.user) + "\n";
				body += "CPU Usage: " + String.valueOf(temp.CPU) + "\n";
				body += "MEM Usage: " + String.valueOf(temp.MEM) + "\n";
				body += "TIME Started: " + String.valueOf(temp.TIME) + "\n";
				body += "Command: " + String.valueOf(temp.command) + "\n";
				body += "\n\n";
            }
            i = 0;
            // To get the array of addresses
            for( String s : emailIDs ) {
                toAddress[i] = new InternetAddress(s);
                i++;
            }
			
            for( int j = 0; j < toAddress.length; j++) {
                message.addRecipient(Message.RecipientType.TO, toAddress[j]);
            }

            message.setSubject(subject);
            message.setText(body);
            Transport transport = session.getTransport("smtp");
            transport.connect(host, from, pass);
            transport.sendMessage(message, message.getAllRecipients());
            transport.close();
            System.out.println("Violated Process details sent successfully");
        }
        catch (AddressException ae) {
            ae.printStackTrace();
        }
        catch (MessagingException me) {
            me.printStackTrace();
        }
    }
}
