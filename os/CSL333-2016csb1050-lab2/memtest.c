#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <limits.h>

int main(){
	int N[] = {10, 20, 40, 80, 160, 320, 640, 1280};
	int K[] = {10, 20, 30, 40, 50, 60 };
	
	clock_t t; // declare the clock object
	
	// variable initialisation for finding the maximum speed params	
	double myRmax_ = 0 ; // max speed
	int myRK_ = 0; // corresponding K
	double myWmax_ = 0 ; // max speed
	int myWK_ = 0; // corresponding K
	int myNR_ = 0;
	int myNW_ = 0;
	for(int i=0 ; i<sizeof(N)/sizeof(N[0]) ; i++){
		
		// variable initialisation for finding the maximum speed params
		double myRmin = INT_MAX ; // minimum clocks for read
		int myRK = 0; // corresponding K
		double myWmin = INT_MAX  ; // minimum clocks for write
		int myWK = 0; // corresponding K
		int myN_ = 0;
		// start the testing 
		for(int j=0 ; j<sizeof(K)/sizeof(K[0]) ; j++){
			printf("\nN = %d K = %d\n" , N[i] , K[j] );
			int Ni = N[i] * 1000000 ;
			char *my_arr = (char*)malloc(sizeof(char)*Ni);
			// Test A
			t = clock(); // start the clock for test A
			for(int k=0 ; k<Ni ; k++){
				*(my_arr+k) = 'a' ; // assign some constant value to each byte
			}
			t = clock() - t ; // end the clock and find the time difference
			// check if this is the minimum for write
			if ( t<myWmin){
				myWmin = t ;
				myWK = 1 ;
			}
			printf("A : %f\n" , ((double)N[i])/(((double)t)/CLOCKS_PER_SEC) );

			// Test B
			t = clock(); // start the clock for test B
			for(int k=0 ; k<Ni ; k+=K[j]){
				if ( k + K[j] >= Ni ){
					memset( my_arr + k , 'a' , Ni-k );
					break;
				}
				memset( my_arr + k , 'a' , K[j]*sizeof(char)); // assign some constant value to each block of K[j] bytes
			}
			t = clock() - t ; // end the clock and find the time difference
			// check if this is the minimum for write
			if ( t<myWmin){
				myWmin = t ;
				myWK = K[j] ;
			}
			printf("B : %f\n" , ((double)N[i])/(((double)t)/CLOCKS_PER_SEC) );
						
			// Test C 
			char tmp = '0' ;
			t = clock(); // start the clock for test C
			for(int k=0 ; k<Ni ; k++){
				tmp = *(my_arr+i) ;  // read value at each byte
			}
			t = clock() - t ; // end the clock and find the time difference
			// check if this is the minimum for read
			if ( t<myRmin){
				myRmin = t ;
				myRK = 1 ;
			}
			printf("C : %f\n" , ((double)N[i])/(((double)t)/CLOCKS_PER_SEC) );

			// Test D
			char *temp = (char*)malloc(sizeof(char)*K[j]);
			t = clock(); // start the clock for test D
			for(int k=0 ; k<Ni ; k+=K[j]){
				if ( k + K[j] >= Ni ){
					memcpy( temp , my_arr+k , Ni-k );
					break;
				}
				memcpy( temp , my_arr+k , K[j]*sizeof(char));  // read value at each block of K[j] bytes
			}
			t = clock() - t ; // end the clock and find the time difference
			// check if this is the minimum for read
			if ( t<myRmin){
				myRmin = t ;
				myRK = K[j] ;
			}
			printf("D : %f\n" , ((double)N[i])/(((double)t)/CLOCKS_PER_SEC) );
			free(my_arr);
		}
		
		double t1 = ((double)N[i])/(((double)myRmin)/CLOCKS_PER_SEC) ;
		double t2 = ((double)N[i])/(((double)myWmin)/CLOCKS_PER_SEC) ;
		
		// Print the maximum speeds and corresponding parameters to console
		printf("\nFor N = %d MB\n" , N[i] );
		printf("Maximum Read Speed = %f for K = %d\n" , t1 , myRK );
		printf("Maximum Write Speed = %f for K = %d\n" , t2 , myWK );
		
		if ( t1 > myRmax_ ){
			myRmax_ = t1 ;
			myRK_ = myRK;
			myNR_ = N[i] ;
		}
		if ( t2 > myWmax_ ){
			myWmax_ = t2 ;
			myWK_ = myWK;
			myNW_ = N[i] ;
		}
	}
	
	printf("\nMaximum Read Speed = %f for N = %d and K = %d\n" , myRmax_ , myNR_ , myRK_ );
	printf("Maximum Write Speed = %f for N = %d and K = %d\n" , myWmax_ , myNW_ , myWK_ );
}
