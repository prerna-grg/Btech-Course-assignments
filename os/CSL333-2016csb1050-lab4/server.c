#include <sys/types.h> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <stdio.h> 
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#define SHMSIZE 1024 

int main() 
{ 
	
	time_t t = time(NULL);
    struct tm tm = *localtime(&t);
	//printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);

    char c; 
    int shmid; 
    key_t key; 
    char *shm, *s; 
    key = 1000 ;
    
    char p[10] ;
    
    printf("You can press Ctrl-C anytime you want to exit.\n");
    
    t = time(NULL);
	tm = *localtime(&t);
	printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
	printf("Waiting for next request...\n\n");
	
    if ((shmid = shmget(key, SHMSIZE, IPC_CREAT | 0666)) < 0)  
    { 
        perror("shmget"); 
        return -1; 
    } 
    
    if ((shm = shmat(shmid, NULL, 0)) == (char *) -1)  
    { 
        perror("shmat"); 
        return -1;
    }
    
    
    while(1){
    	while (*shm != '*'){
		    sleep(1);
		}
		/* read from shm to fill the buffer */
		int i=0;
		s = shm ;
		s++;
		
        char buffer[100];
        strcpy(buffer , s);
       
        s = shm;
        *s = '#'; // wait till client changes it
        
       	t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf("Request received for: %s\n",buffer ); 
				
       	t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf("Contacting Web service...\n");
		
		char url[1000];
		strcpy(url, "wget -q http://free.currencyconverterapi.com/api/v5/convert?q=INR_");
		strcat(url, buffer);
		strcat(url,"&compact=y");
		system(url); 
		sleep(2);
		
		FILE *file;
		char *code = malloc(1000 * sizeof(char));
		char* w = code;
		char filename[100];
		strcpy(filename, "convert?q=INR_");
		strcat(filename , buffer);
		
		file = fopen(filename, "r");
		
		if(!file){
			t = time(NULL);
			tm = *localtime(&t);
			printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
			printf("Could not fetch the conversion\n");
			t = time(NULL);
			tm = *localtime(&t);
			printf("\n[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);

			printf("Waiting for next request...\n\n");
			s = shm;
			s++;
			strcpy(s,"FAILED");
			s = shm;
			*s = '@';
			continue;
		}
		
		int start = 0;
		int flag=0;
		do 
		{
			char c = (char)fgetc(file);
			if(c==EOF)break; 
			if ( start == 0 && c == 'v' ){
				start ++;
			}
			else if ( start == 1 && c == 'a' ){
				start ++;
			}
			else if ( start == 2 && c == 'l' ){
				start ++;
			}
			else if ( start == 3 && c == '"' ){
				start ++;
			}
			else if ( start == 4 && c == ':' ){
				start ++;
			}else if( start == 5 && c == ',' ){
				*w = '\0';
				flag=1;
				break;
			}
			else if( start == 5 && c == '}' ){
				*w = '\0';
				flag=1;
				break;
			}
			else if ( start == 5 && c != ',' ){
				*w++ = c ;
			}
			else if ( start == 5 && c != '}' ){
				*w++ = c ;
			}
			else{
				start = 0;
			}
		} while(1);
		fclose(file);
		if(flag==0){
			t = time(NULL);
			tm = *localtime(&t);
			printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
			printf("Could not fetch the conversion\n");
	       	t = time(NULL);
			tm = *localtime(&t);
			printf("\n[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
			printf("Waiting for next request...\n");
			s = shm;
			s++;
			strcpy(s,"FAILED");
			s = shm;
			*s = '@';
			continue;
		}
		
		char buf[100];
		w = code;
		strcpy(buf,w);
		t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf("INR_%s conversion is %s.\n" , buffer , buf );
       	t = time(NULL);
		tm = *localtime(&t);
		printf("\n[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf("Waiting for next request...\n\n");
		s = shm;
		s++;
    	for ( int i=0 ; i<strlen(buf) ; i++){
        	*s++ = buf[i];
        }
        *s = '\0';
        s = shm;
        *s = '@' ;
        
	}
  
    return 0;
    
} 
    
