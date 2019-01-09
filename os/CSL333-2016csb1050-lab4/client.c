#include <sys/types.h> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <stdio.h> 
#include <string.h>
#include <sys/types.h> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <stdio.h> 
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#define SHMSIZE  1024

int main() 
{ 
	time_t t = time(NULL);
    struct tm tm = *localtime(&t);
	
    int shmid; 
    key_t key; 
    char *shm, *s ; 
    char buffer[500];
    char c;
    key = 1000 ; 
    
    if ((shmid = shmget(key, SHMSIZE, 0666)) < 0) { 
        perror("shmget"); 
        return -1;
    }
    
    if ((shm = shmat(shmid, NULL, 0)) == (char *) -1) { 
        perror("shmat"); 
        return -1; 
    } 
    printf("You can press Ctrl-C anytime you want to exit.\n");
    s = shm ;
    *s = '#' ;
    while(1){
    	char curr[100];
    	
		t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf( "Currency code (e.g. USD, GBP, etc.): " );

		scanf("%s" , curr);
		s = shm+1;
    	for ( int i=0 ; i<strlen(curr) ; i++){
        	*s++ = curr[i];
        }
        *s = '\0';
        s = shm;
		*s = '*' ;
       	t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
		printf( "Waiting for server’s response...\n" );
		while (*s != '@'){
		    sleep(1);
		}
		
		int j=0;
		s++;
		char out[100];
		strcpy(out,s);
       	t = time(NULL);
		tm = *localtime(&t);
		printf("[%d-%d-%d %d:%d:%d] ", tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
        printf("Conversion rate wrt INR: %s\n\n",out );
	}   
    
    return 0; 
} 


       
