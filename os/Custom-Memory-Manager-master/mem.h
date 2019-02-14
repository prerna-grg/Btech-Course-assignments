#ifndef mem_H
#define mem_H
#include<sys/resource.h>
#include <stdio.h>
#include<unistd.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>

typedef struct node Heap;
struct node{
	bool free ;
	size_t size ;
	Heap* prev ;
	Heap* next ;
	void *block ;
} ;

void *csl333_malloc(size_t size);

void csl333_free(void *ptr);

void *csl333_realloc(void *ptr,size_t size);

#endif
