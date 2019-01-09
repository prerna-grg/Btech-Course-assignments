#include<sys/resource.h>
#include <stdio.h>
#include<unistd.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include "mem.h"

// global variable for heap
Heap *my_mem = NULL;

// increment the given address by the given bytes
void* moveBytes( void* ptr , int increment ){
	char* c = (char*)ptr;
	c = c + increment ;
	return (void*)c;
}

// print the linked list to check implementation
void checkMetaData(){
	Heap* my_heap = my_mem ;
	while(my_heap!=NULL){
		printf("%lu %d\n" , my_heap->size , my_heap->free );
		my_heap = my_heap->next ;
	}
	printf("\n");
}

// My implementation of malloc
void* csl333_malloc(size_t size){

	if (size<=0)return NULL; // nothing to allocate
	if(my_mem == NULL){
		
		/* move sbrk to get bytes */
		my_mem = sbrk( sizeof(Heap)); 
		
		/* set the variables */
		my_mem->size = size ; 
		my_mem->free = false;
		my_mem->prev = NULL;
		my_mem->next = NULL;
		my_mem->block = sbrk(size);
		
		/* initialise all bytes to 0 */
		memset( my_mem->block , 0 , size );
		return my_mem->block;
	}
	
	Heap* temp = my_mem ;
	while( temp->next!=NULL ){
		if (temp->size >= size && temp->free==true) {
			// found an already existing block to allocate
			if (temp->size > size + sizeof(Heap) ){
				// fragment this block into 2 parts (2nd one is a residual node)
				
				/* Make the residual node */
				Heap* res = (Heap*)moveBytes(temp->block , size );
				res->free = true ;
				res->size  = temp->size - size - sizeof(Heap) ;
				res->prev = temp ;
				res->next = temp->next ;
				if( temp->next != NULL){
					temp->next->prev = res ;
				}
				
				/* Set value of the allocated node */
				temp->next = res ;
				temp->free = false;
				temp->size = size ;
				res->block = moveBytes( temp->block , size + sizeof(Heap) );
				/* initialise all bytes to 0 */
				memset( temp->block , 0 , size );
				return temp->block ;
			}else{
				temp->free = false;
				/* initialise all bytes to 0 */
				memset( temp->block , 0 , size );
				return temp->block ;
			}
		}
		temp = temp->next;
	}
	
	// Now you are in the last mapped block
	// check if you can allocate here
	if (temp->size >= size && temp->free==true) {
		if (temp->size > size + sizeof(Heap) ){
			// fragment this block into 2 parts (2nd one is a residual node)
			Heap* res = (Heap*)moveBytes(temp->block , size );
			res->free = true ;
			res->size  = temp->size - size - sizeof(Heap) ;
			res->prev = temp ;
			res->next = temp->next ;
			if( temp->next != NULL){
				temp->next->prev = res ;
			}
			temp->next = res ;
			temp->free = false;
			res->block = moveBytes( temp->block , size + sizeof(Heap) );
			memset( temp->block , 0 , size );
			return temp->block ;
		}else{
			temp->free = false;
			memset( temp->block , 0 , size );
			return temp->block ;
		}
	}
	// nothing in the mapped region is empty : use sbrk
	Heap* newNode = sbrk( sizeof(Heap) );
	if(newNode == (void*)-1 ){
		int s = brk(sbrk(0)+sizeof(Heap));
	}
	// try again
	newNode = sbrk( sizeof(Heap) );
	
	newNode->block = sbrk( size );
	if(newNode->block == (void*)-1){
		// try moving the hard limit
		int s = brk(sbrk(0)+size);
	}
	// try again
	newNode->block = sbrk( size );
	// if still not enough : return null
	if(newNode == (void*)-1 || newNode->block == (void*)-1){
		return NULL;
	}
	newNode->size = size ;
	newNode->free = false ;
	newNode->prev = temp ;
	newNode->next = NULL ;
	temp->next = newNode ;
	memset( newNode->block , 0 , size );
	return newNode->block ;
}

// My implementation of free
void csl333_free(void *ptr){
	/* Nothing to free */
	if (ptr==NULL || my_mem==NULL){
		return;
	}
	/* find the block to be freed */
	Heap* temp = my_mem ;
	while(temp->block!=ptr){
		/* No such block exists : return*/
		if ( temp->next == NULL){
			return ;
		}
		temp = temp->next ;
	}
	/* block found : free it */
	temp->free = true;
	
	/* Coalesce if the block above is free */
	if (temp->next != NULL ){
		if ( temp->next->free == true ){
			temp->size = temp->size + sizeof(Heap) + temp->next->size ;
			temp->next = temp->next->next ;
			if(temp->next!=NULL){
				temp->next->prev = temp;
			}
		}
	}
	
	/* Coalesce if the block below is free */
	if (temp->prev != NULL ){
		if ( temp->prev->free == true ){
			temp = temp->prev ;
			temp->size = temp->size + sizeof(Heap) + temp->next->size ;
			temp->next = temp->next->next ;
			if(temp->next!=NULL){
				temp->next->prev = temp;
			}
		}
	}
	
	if ( temp->next == NULL ){
		if(temp->prev!=NULL){
			temp->prev->next = NULL;
			temp = NULL;
		}
		else{
			my_mem = NULL ;
		}
	}
}

// My implementation of realloc
void* csl333_realloc(void* ptr, size_t size){
	if ( size==0 && ptr==NULL)return NULL;
	else if ( ptr == NULL )return csl333_malloc(size);
	else if( size==0 ){
		csl333_free(ptr);
		return NULL;
	}else{
		size_t prevSize = 0;
		Heap *temp = my_mem;
		while(temp != NULL){
			if(temp->block == ptr) {
				prevSize = temp->size;
				break;
			}
			temp = temp->next;
		}
		if ( temp==NULL ){
			return ptr;
		}
		if ( prevSize == size ){
			return ptr; // nothing new to allocate 
		}
		char array[prevSize] ; // take some memory from local stack
		for (int i=0 ; i<prevSize ; i++){
			array[i] = *((char*)ptr+i) ;
		}
		csl333_free(ptr) ;
		void* new_block = csl333_malloc(size);
		
		/* If new block could not be created then recreate the previous block and return */
		if (new_block == NULL){
			ptr = csl333_malloc(prevSize);
			memcpy( ptr , array , prevSize );
			return ptr ;
		}
		
		/* If successfully created then copy the pre-existing data and return the new block */
		if(prevSize < size ){
			memcpy( new_block , array , prevSize );
		}else{
			memcpy( new_block , array , size );
		}
		return new_block ;
	}
}

