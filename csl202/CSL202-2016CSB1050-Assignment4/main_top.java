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
import java.lang.StringBuilder;
import java.util.HashMap;
import java.util.Map;
import top.Emails;
import top.processDetail;

public class main_top{
	
	public static void main(String args[]) throws Exception {

		String fileName = "settings.properties"; // file containing information of all constraints
		String line = null;
		int n2_= 0; // temporary variable for quota.window.minutes
		float conditions[] = new float[5];
		ArrayList<String> emailIDs = new ArrayList<String>(); // Email addresses to be notified in case of violations
		try{
			FileReader fileReader = new FileReader(fileName);
		    BufferedReader bufferedReader = new BufferedReader(fileReader);
		    
		    // reading file settings.properties to get all the constraints
		    while((line = bufferedReader.readLine()) != null) {
		    	String ar[] = line.split("\\s+");
		    	if(ar.length!=3)continue;
		    	if(ar[0].equals("quota.window.minutes")){
		    		n2_ = Integer.parseInt(ar[2]);
		    	}else if(ar[0].equals("sustained.max.cpu.usage.duration.limit")){
		    		conditions[1] = Integer.parseInt(ar[2]);
		    	}else if(ar[0].equals("sustained.max.cpu.usage.limit")){
		    		conditions[2] = Integer.parseInt(ar[2]);
		    	}else if(ar[0].equals("sustained.max.memory.usage.duration.limit")){
		    		conditions[3] = Integer.parseInt(ar[2]);
		    	}else if(ar[0].equals("sustained.max.memory.usage.limit")){
		    		conditions[4] = Integer.parseInt(ar[2]);
		    	}else if(ar[0].equals("notify.emails")){
		    		String notify_emails[] = ar[2].split(",");
		    		for(String s : notify_emails)emailIDs.add(s);
		    	}
		    }
		    bufferedReader.close();
		}catch(FileNotFoundException ex) {
			System.out.println("Error: settings.properties Missing");
		}


		int n2 = n2_; //quota.window.minutes
        float cpu_usage_d_limit = conditions[1]; //sustained.max.cpu.usage.duration.limit
        float cpu_usage_limit = conditions[2]; //sustained.max.cpu.usage.limit
        float mem_usage_d_limit = conditions[3]; // sustained.max.memory.usage.duration.limit
        float mem_usage_limit = conditions[4]; // sustained.max.memory.usage.limit
		
		// file storing historical information of top command
		String topFile = "history_info.txt";
		HashMap<Integer,processDetail> procData = new HashMap<>(); // stores running processes information
		HashMap<Integer,processDetail> violators = new HashMap<>(); // stores violating processes information
		
		int n1 = 30; // run top command every 30 seconds
		// can be changed but should be less than 60 seconds
		
        /* service_top runs runnable_top every n1(defined above) seconds.. It runs the top command to gather information of
        all the currently running processes and stores them in the procData list and append it to top.txt and service_read
        runs runnable_read every n2(defined above) seconds.. It reads the top file to find those top commands that had been
        run before n2 seconds and deletes their data i.e. it acts like a garbage collector coming every few minutes/seconds to
        clean */
        ScheduledExecutorService service_top = Executors.newSingleThreadScheduledExecutor();
		ScheduledExecutorService service_read = Executors.newSingleThreadScheduledExecutor();

		Runnable runnable_top = new Runnable(){
			public void run(){
				//if(!service_read.isShutdown())return;
				try{
                    // run top command to gather information
                    System.out.println("Top Command Running....");
					List<String> cmdList = new ArrayList<String>();
					cmdList.add("top");
					cmdList.add("-n1");
					cmdList.add("-b");
					ProcessBuilder pb = new ProcessBuilder(cmdList);
					Process p = pb.start();
                    // output of top command stored in an inputstream
					InputStream fis = p.getInputStream();
					BufferedReader reader = new BufferedReader(new InputStreamReader(fis));
					String line; 
				    BufferedWriter out = new BufferedWriter(new FileWriter(topFile , true));
                    // get the current date and time to be stored along with historical information
					SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
					Date date = new Date();
					String currDate = formatter.format(date); // format the date as required
					currDate.replace("T" , " ");
					// print the current date/time to the file explicitly as top command does not print date 
					out.write("\n\n" + "DateTime: " +  currDate + "\n");
					
					// store all processes currently given by top
					HashMap<Integer,processDetail> childData = new HashMap<>();
					while ((line = reader.readLine()) != null){
						line = line.trim();
						out.write(line);
						out.write("\n");
						String arr[] = line.split("\\s+");
						
						// For processes with name having >1 tokens
						if(arr.length > 12){
							for(int i=12 ; i<arr.length ; i++){
								arr[11] = arr[11] + " " ;
								arr[11] = arr[11] + arr[i];
							}
						}
						
						String rgx = "[0-9]+";
						//Regular expression to find which line is process information i.e. looking for PID
                        Pattern pattern = Pattern.compile(rgx);
                        Matcher matcher = pattern.matcher(arr[0]);
                        // top -n1 b command will give 12 columns as output
                        // this fact is used to exclude lines other than processes from the reading
                        if(!matcher.find() || arr.length<12){
                            continue;
                        }
						Integer currentPID = Integer.parseInt(arr[0]);
                        processDetail temp = new processDetail();

                        // add data to the instance
                        temp.setPID(currentPID);
                        temp.setUser_COMM_TIME(arr[1],arr[11],arr[10]);
                        temp.setCPU_MEM(Float.valueOf(arr[8]),Float.valueOf(arr[9]));
                        
                        if(temp.CPU > cpu_usage_limit)temp.setVTC(n1);
                        else temp.setVTC(0);
                        if(temp.MEM > mem_usage_limit)temp.setVTM(n1);
                        else temp.setVTM(0);
                        
                        childData.put(currentPID,temp);
                        // if the process already exists in the procData update its cpu usage and cpu usage duration limit
                        if(procData.containsKey(currentPID)){
                        	String u1 = (procData.get(currentPID)).user ;
                   			String c1 = (procData.get(currentPID)).command;
                   			// The point here is lets say a process P1 executed and successfully shut down, now its process ID is avaliable for any new process coming up, so when we are checking whether it is the same old process we should compare user and command name also
                   			if( arr[1].equals(u1) && arr[11].equals(c1)){
						    	if(temp.CPU > cpu_usage_limit){
						    		int vtc = (procData.get(currentPID)).cpu_violation_time + n1;
						    		temp.setVTC(vtc);
						    		if(vtc > cpu_usage_d_limit ){
						    			violators.put(currentPID,temp);
						    			/* if violation has occurred once mail would be sent and now the process use timing would be set to zero, otherwise it would keep sending mail every 30 seconds which is not our purpose*/
						    			temp.setVTC(0);
						    		}
						    	}
						    }
                        }
                        // if the process already exists in the procData update its mem usage and mem usage duration limit
                        if(procData.containsKey(currentPID)){
                   			String u1 = (procData.get(currentPID)).user ;
                   			String c1 = (procData.get(currentPID)).command;
                   			// The point here is lets say a process P1 executed and successfully shut down, now its process ID is avaliable for any new process coming up, so when we are checking whether it is the same old process we should compare user and command name also
                   			if( arr[1].equals(u1) && arr[11].equals(c1)){
		                    	if(temp.CPU > mem_usage_limit){
		                    		int vtm = (procData.get(currentPID)).mem_violation_time + n1;
		                    		temp.setVTM(vtm);
		                    		if(vtm > mem_usage_d_limit ){
		                    			violators.put(currentPID,temp);
		                    			/* if violation has occurred once mail would be sent and now the process use timing would be set to zero, otherwise it would keep sending mail every 30 seconds which is not our purpose*/
		                    			temp.setVTM(0);
		                    		}
		                    	}
		                    }
                        }
                     	procData.put(currentPID , temp); // add to the map of currently running processes
					}
					List<Integer> to_remove = new ArrayList<>();
					for (Integer ID : procData.keySet()){
                    	if(!childData.containsKey(ID)){
                    		// Process has finished
                    		to_remove.add(ID);
                    	}
                    }
                    for( int i : to_remove)procData.remove(i); // remove the processes that have shut down
					out.write("\n");
					out.close();
					System.out.println("Top Command output stored in history_info.txt");
                    // send emails to the registered users of all the violated processes
                    if(violators.size()!=0){
		                Emails emails = new Emails();
		                emails.sendEmails(violators , emailIDs);
						violators.clear();
					}
				}catch (IOException e) {
					e.printStackTrace();
				}
			}
		};
		
		Runnable runnable_read = new Runnable(){
			public void run(){
				System.out.println("Cleaning past " + n2 + " minutes data....");
				//if(!service_top.isShutdown())return;
				SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                // get the current date_time to check for violations
				Date date = new Date();
				String currDate = formatter.format(date);// formatting
				currDate.replace("T" , " ");
				StringBuilder sb = new StringBuilder();
				try{
					// open file to read data
					FileReader file = new FileReader(topFile);
		        	BufferedReader br = new BufferedReader(file);
					String line1;
		        	int flag = 0;
					while((line1 = br.readLine()) != null) {
						line1 = line1.trim();
		        		String arr[] = line1.split("\\s+");
		        		// find if the line prints date-time to check if that top command is within n2 minutes range or not
		        		if(arr.length==3 && arr[0].equals("DateTime:")){
		        			flag = 0;
		        			String fileDate = arr[1];
		        			fileDate += " ";
		        			fileDate += arr[2];
		        			Date d1 = null;
		        			Date d2 = null;
		        			try {
								d2 = formatter.parse(currDate);
								d1 = formatter.parse(fileDate);
								/* difference between 2 dates in seconds to calculate how much time has passed since this
								top command generated its output */
								long diff = d2.getTime() - d1.getTime(); // time passed
								long diffSeconds = diff/1000%60;
								long diffMinutes = (diff/(60*1000)%60)*60;
								long diffHours = (diff/(60*60*1000)%24)*60*60;
								long diffDays = (diff/(24*60*60*1000))*24*60*60;
								diff = diffSeconds + diffMinutes + diffHours + diffDays; // in seconds
								if(diff > n2*60 ){
									flag = 1; // remove all following lines until the next top from the file
								}else{
									sb.append(line1);
									sb.append("\n");
								}
							}catch (Exception e){
								e.printStackTrace();
							}
		        		}else{
		        			if(flag==1){
		        				continue;
		        			}else{
		        				sb.append(line1);
		        				sb.append("\n");
		        			}
		        		}
			        }
                    // re-enter into file
			        PrintWriter writer = new PrintWriter(topFile);
			        String s = sb.toString();
					writer.print(s);
				}catch(FileNotFoundException e){
					e.printStackTrace();
				}catch(IOException e){
					e.printStackTrace();
				}
			}
		};
		// executor object to run instructions periodically
		service_top.scheduleAtFixedRate(runnable_top, 0, n1 , TimeUnit.SECONDS);
    	service_read.scheduleAtFixedRate(runnable_read, 0, n2 , TimeUnit.MINUTES);
	}
}
