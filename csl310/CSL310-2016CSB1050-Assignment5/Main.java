import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.Scanner;
import javax.persistence.EntityManager;
import javax.persistence.Query;

public class Main {

    private EntityManagerFactory emf = null;
    private static final List<Date> dates = new ArrayList<>();
    
    // Class constructor
    public Main() {
        emf = Persistence.createEntityManagerFactory("JavaApplication1PU");
    }

	// if data is already present adding again would induce inconsistency, this function avoids the same
	public int checkDatabase(){
    	List<Team> list = null;
        EntityManager em = emf.createEntityManager();
        try {
            Query q = em.createNamedQuery("Team.findAll"); // check any table to see if data exists
            list = q.getResultList();
            if( list.size() > 0 )return 1; // data present
        } finally {
            em.clear();
            em.close();
        }
        return 0; // data not present
    }
    
    // generic function to sace data to the database
    public <E> void saveEntity(E entity){
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            em.persist(entity);
            em.getTransaction().commit();
        } catch (Exception e) {
            em.getTransaction().rollback();
            em.close();
        } finally {
            em.close();
        }
    }
    
    // query to find number of players in a given team with salary in a given range
    public List<Object[]> findPlayersInSalaryRange(String team_name , int min , int max) {
    	List<Object[]> list = null;
        EntityManager em = emf.createEntityManager();
        try {
            Query q = em.createNamedQuery("TeamMember.findPlayersInSalaryRange"); // query
            q.setParameter(1, team_name); // parameters
            q.setParameter(2, min); // parameters
            q.setParameter(3, max); // parameters
            list = q.getResultList(); // result is retrieved as a list of object arrays
        } finally {
            em.clear();
            em.close();
        }
        return list;
    }
    
    // query to find members by role in a given team
    public List<Object[]> findMembersByRole(String team_name){
    	List<Object[]> list = null;
        EntityManager em = emf.createEntityManager();
        try {
            Query q = em.createNamedQuery("TeamMember.findCountByRole");
            q.setParameter(1, team_name); // parameters
            list = q.getResultList(); // result is retrieved as a list of object arrays
        } finally {
            em.clear();
            em.close();
        }
        return list;
    }
    
    // query to find average salary of players in a given state
    public List<Object[]> findAvgSalaryInState(String State){
    	List<Object[]> list = null;
        EntityManager em = emf.createEntityManager();
        try {
            Query q = em.createNamedQuery("TeamMember.findAvgStateSalary");
            q.setParameter(1, State); // parameters
            list = q.getResultList(); // result is retrieved as a list of object arrays
        } finally {
            em.clear();
            em.close();
        }
        return list;
    }
    
    // generates new contacts by reading some data from data_files 
    public static List<Contactinformation> getNewContacts(int no_of_contacts) {
        List<Contactinformation> contacts = new ArrayList<>();
        String fileName = "cities.txt"; // names of cities
        List<String> Cities = new ArrayList<>(); // list of cities
        List<String> States = new ArrayList<>(); // list of the corresponding states of cities
        try{
            FileReader fileReader = new FileReader(fileName);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;
            while( (line = bufferedReader.readLine()) != null) {
                    Cities.add(line); // list of cities
            }	
            fileName = "states.txt"; // names of states
            fileReader = new FileReader(fileName);
            bufferedReader = new BufferedReader(fileReader);
            while( (line = bufferedReader.readLine()) != null) {
                    States.add(line); // list of states
            }
            int s=0;
            // generating Contact_information object
            for(int i=0 ; i<no_of_contacts ; i++){
                RandomData rnd = new RandomData();
                Contactinformation temp = new Contactinformation();
                temp.setStreetAddress("Street No. 5");
                temp.setCity(Cities.get(s));
                temp.setState(States.get(s));
                s++;
                temp.setCountry("India");
                temp.setPostalCode(rnd.getPost()); // get randomly generated postal code
                temp.setMobile(rnd.getMob()); // get randomly generated mobile number
                temp.setPhone("add number");
                temp.setEmail(rnd.getMail()); // get randomly generated email 
                contacts.add(temp); // add the object to the list to be returned
            }
        }catch(FileNotFoundException ex) {
            System.out.println("Missing files"); // .txt files missing
        }catch (IOException e) {
            System.out.println(e.toString());
        }
        return contacts;
    }
    
    // generates new teams by reading some data i.e. team names from data_files 
    private static List<Team> getNewTeams(List<Contactinformation> generated_contacts){
    	Random random = new Random();
    	List<Team> teams = new ArrayList<>(); // list of teams
    	try{
            FileReader fileReader = new FileReader("teams.txt");
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;
            int i=0;
            while( (line = bufferedReader.readLine()) != null) {
                RandomData rnd = new RandomData();
                Team temp = new Team();
                temp.setStatus("Active");
                int index = random.nextInt(generated_contacts.size()); // random contact id
                temp.setOffice(generated_contacts.get(index)); // get the contact from id
                temp.setName(line); // random name
                temp.setCreationDate(rnd.getDate(2010,2012)); // random creation date
                dates.add(temp.getCreationDate()); // record of creation dates to be used while assigning members
                i++;
                teams.add(temp);
                if(i==20)break;
            }
        }catch(FileNotFoundException ex) {
            System.out.println("Missing files"); // .txt file with team names missing
        }catch (IOException e) {
            System.out.println(e.toString());
        }

        return teams;
    }
    
    // generate random persons 
    private static List<Person> getNewDummyPerson(List<Contactinformation> generated_contacts) {
        Random random = new Random();
        List<Person> persons = new ArrayList<>(); // person object list 
        List<String> sur_names = new ArrayList<>(); // sur names list
        List<String> names = new ArrayList<>(); // names list

        String fileName = "dummy_sur_names.txt"; // sur names file
        try{
            FileReader fileReader = new FileReader(fileName);
            BufferedReader bufferedReader = new BufferedReader(fileReader);
            String line;
            while( (line = bufferedReader.readLine()) != null) {
                    sur_names.add(line); // surnames
            }
            fileName = "dummy_names.txt"; // names file
            fileReader = new FileReader(fileName);
            bufferedReader = new BufferedReader(fileReader);
            while( (line = bufferedReader.readLine()) != null) {
                    names.add(line); // names
            }

            for(int i=0 ; i<600 ; i++){
                RandomData rnd = new RandomData();
                Person tmp = new Person();
                tmp.setFirstname(names.get(random.nextInt(names.size()))); // random name
                tmp.setLastname(sur_names.get(random.nextInt(sur_names.size()))); // random sur name
                tmp.setDoB(rnd.getDate(1980,1995)); // random birth date
                int index = random.nextInt(generated_contacts.size()); // random contact id
                tmp.setContact(generated_contacts.get(index)); // get contact using id
                persons.add(tmp);
            }

        }catch(FileNotFoundException ex) {
            System.out.println(ex.toString());
        }catch (IOException e) {
            System.out.println(e.toString());
        }
        return persons;
    }
    
    // generate team members randomly for the teams
    private static List<TeamMember> getNewTeamMembers(List<Person> generated_persons , List<Team> generated_teams){
    	Random random = new Random();
    	List<TeamMember> team_mems = new ArrayList<>();
    	int i=1;
    	while( i<= 20 ){
            int i1 = random.nextInt(5) + 10; // random number of players between 10 and 15
            int i2 = random.nextInt(3) + 2; // random number of managers between 2 and 5
            int i3 = random.nextInt(3) + 2; // random number of owners between 2 and 5
            int i4 = random.nextInt(4); // random number of others between 0 and 4
            int g=0;
            HashMap<Integer,Integer> ids = new HashMap<>();
            // get random ids of persons to assign to teams
            while(g<i1+i2+i3+i4){
                int tm = random.nextInt(600);
                if(ids.containsValue(tm)){
                    // do nothing and find another candidate, repeated not consistent
                }else{
                    ids.put(g,tm); // valid id
                    g++;
                }
            }
            g=0;
            // assign players
            for(int f=0;f<i1;f++){
                TeamMember temp = new TeamMember();
                temp.setTeamID(generated_teams.get(i-1)); // get team id
                temp.setPersonID(generated_persons.get(ids.get(g))); // get person id
                g++;
                temp.setSalary(random.nextInt(500000) + 100000); // random salary >100000
                temp.setHireDate(dates.get(i-1)); // get dates for hiring after the team has been created
                Date currDate = new java.sql.Date(temp.getHireDate().getTime());
                Calendar c = Calendar.getInstance();
                c.setTime(currDate);
                int day = c.get(Calendar.DAY_OF_MONTH);
                int month = c.get(Calendar.MONTH);
                int year = c.get(Calendar.YEAR);
                GregorianCalendar startdate = new GregorianCalendar(year,month,day);
                startdate.add(GregorianCalendar.DATE, random.nextInt(7)); // add random delay upto 7 days from creation date
                temp.setHireDate(startdate.getTime());
                temp.setRole("Player");
                temp.setRemarks("Awesome Player :-P"); // remarks
                team_mems.add(temp);
            }
            for(int f=0;f<i2;f++){
                TeamMember temp = new TeamMember();
                temp.setTeamID(generated_teams.get(i-1)); // get team id
                temp.setPersonID(generated_persons.get(ids.get(g))); // get person id
                g++;
                temp.setSalary(random.nextInt(500000) + 100000); // random salary >100000
                temp.setHireDate(dates.get(i-1)); // get dates for hiring after the team has been created
                Date currDate = new java.sql.Date(temp.getHireDate().getTime());
                Calendar c = Calendar.getInstance();
                c.setTime(currDate);
                int day = c.get(Calendar.DAY_OF_MONTH);
                int month = c.get(Calendar.MONTH);
                int year = c.get(Calendar.YEAR);
                GregorianCalendar startdate = new GregorianCalendar(year,month,day);
                startdate.add(GregorianCalendar.DATE, random.nextInt(7)); // add random delay upto 7 days from creation date
                temp.setHireDate(startdate.getTime());
                temp.setRole("Manager");
                temp.setRemarks("Hard-working Manager :-)"); // remarks
                team_mems.add(temp);
            }
            for(int f=0;f<i3;f++){
                TeamMember temp = new TeamMember();
                temp.setTeamID(generated_teams.get(i-1)); // get team id
                temp.setPersonID(generated_persons.get(ids.get(g))); // get person id
                g++;
                temp.setSalary(random.nextInt(500000) + 100000); // random salary >100000
                temp.setHireDate(dates.get(i-1)); // get dates for hiring after the team has been created
                Date currDate = new java.sql.Date(temp.getHireDate().getTime());
                Calendar c = Calendar.getInstance();
                c.setTime(currDate);
                int day = c.get(Calendar.DAY_OF_MONTH);
                int month = c.get(Calendar.MONTH);
                int year = c.get(Calendar.YEAR);
                GregorianCalendar startdate = new GregorianCalendar(year,month,day);
                startdate.add(GregorianCalendar.DATE, random.nextInt(7)); // add random delay upto 7 days from creation date
                temp.setHireDate(startdate.getTime());
                temp.setRole("Owner");
                temp.setRemarks("Strict Owner :-("); // remarks
                team_mems.add(temp);
            }
            for(int f=0;f<i4;f++){
                TeamMember temp = new TeamMember();
                temp.setTeamID(generated_teams.get(i-1)); // get team id
                temp.setPersonID(generated_persons.get(ids.get(g))); // get person id
                g++;
                temp.setSalary(random.nextInt(500000) + 100000); // random salary >100000
                temp.setHireDate(dates.get(i-1)); // get dates for hiring after the team has been created
                Date currDate = new java.sql.Date(temp.getHireDate().getTime());
                Calendar c = Calendar.getInstance();
                c.setTime(currDate);
                int day = c.get(Calendar.DAY_OF_MONTH);
                int month = c.get(Calendar.MONTH);
                int year = c.get(Calendar.YEAR);
                GregorianCalendar startdate = new GregorianCalendar(year,month,day);
                startdate.add(GregorianCalendar.DATE, random.nextInt(7)); // add random delay upto 7 days from creation date
                temp.setHireDate(startdate.getTime());
                temp.setRole("Other");
                temp.setRemarks("Boring Other :/"); // remarks
                team_mems.add(temp);
            }
            i++;
    	}
    	return team_mems;
    }
    
    // Main function to execute all calls
    public static void main(String[] args) throws IOException {
    	if( args.length!=1 ){
    		System.out.println("Invalid run\nFormat: java -cp \\*:. Main -i or -q");
    		return;
    	}
        Main app = new Main();
    	if( args[0].equalsIgnoreCase("-i")){
    		int ch = app.checkDatabase();
    		if( ch==1){
    			System.out.println("Data already present"); // data cannot be repeated other wise it would be inconsistent
    			return;
    		}
    		
    		// get 20 new contacts
		    List<Contactinformation> Contacts = getNewContacts(20);
		    for (Contactinformation c : Contacts){
		        app.saveEntity(c); // save in the database
		    }
		    System.out.println("Saved "+ Contacts.size() + " new contacts.");
		    
		    // get new Persons
		    List<Person> Persons = getNewDummyPerson(Contacts);
		    for (Person p : Persons){
		        app.saveEntity(p);// save in the database
		    }
		    System.out.println("Saved "+ Persons.size() + " new persons.");
		    
		    // get 20 new teams
		    List<Team> Teams = getNewTeams(Contacts);
		    for (Team t : Teams){
		        app.saveEntity(t);// save in the database
		    }
		    System.out.println("Saved " + Teams.size() +" new teams.");
		    
		    // get new team members 
		    List<TeamMember> members = getNewTeamMembers(Persons,Teams);
		    for (TeamMember m : members){
		        app.saveEntity(m);// save in the database
		    }
		    System.out.println("Saved " + members.size() +" new team members.");
    		
    	}else if( args[0].equalsIgnoreCase("-q")){
    		System.out.println("Enter 1 to find all Players of a given Team whose salary is between a given range\n"
                + "Enter 2 to find Role wise numbers of team members in a given team.\n"
                + "Enter 3 to find average salary of players from a given state.");
        
	        Scanner scan = new Scanner(System.in);
			int query = scan.nextInt(); // number of query
			switch (query) {
				case 1:
					{
					    System.out.print("Enter team Name: "); // get user input team name
					    BufferedReader br2 = new BufferedReader(new InputStreamReader(System.in));
					    String team_name = br2.readLine();
					    System.out.print("Enter Min Salary: "); // get user input min salary
					    int min = scan.nextInt();
					    System.out.print("Enter Max Salary: "); // get user input max salary
					    int max = scan.nextInt();
					    List<Object[]> out = app.findPlayersInSalaryRange(team_name, min, max);
					    System.out.println("Got "+out.size()+" records.");
					    // printing the retreived data
					    if(out.size()!=0){
					        System.out.println("\nPlayers in team " + team_name + " with salary between " + min + " and " + max + " are:");
					        String output2 = String.format("%-20s: %-15s %s" , "Player Name" , "Hire Date" , "Salary"  ) ;
					        System.out.println(output2);
					    }
					    for(Object[] o : out){
					        
					        String output = String.format("%-20s: %-15s %d" , (String)o[0]+" "+(String)o[1] , (java.sql.Date)o[2] , (Integer)o[3] ) ;
					        System.out.println(output);
					    }
					    break;
					}
				case 2:
					{
					    System.out.print("Enter Team Name: ");// get user input team name
					    BufferedReader br2 = new BufferedReader(new InputStreamReader(System.in));
					    String team_name = br2.readLine();
					    List<Object[]> out = app.findMembersByRole(team_name);
					    System.out.println("Got "+out.size()+" rows.");
					    // printing the retreived data
					    for(Object[] o : out){
					        String output = String.format("%-5s: %-10s %-8s: %s" ,"Role", (String)o[0] ,"Members" ,(Long)o[1]) ;
					        System.out.println(output);
					    }
					    break;
					}
				case 3:
					{
					    System.out.print("Enter State Name: ");// get user input state name
					    BufferedReader br2 = new BufferedReader(new InputStreamReader(System.in));
					    String state = br2.readLine();
					    List out = app.findAvgSalaryInState(state);
					    // printing the retreived data
					    System.out.println("\nAverage Salary in " + state + " is: " + out + "\n");
					    break;
					}
				default:
					break;
			}	
    	}
    }
}
