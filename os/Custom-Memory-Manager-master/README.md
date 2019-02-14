# Custom-Memory-Manager

C Implementation of malloc , realloc and free

1. What does this program do
I have implemented three functions malloc , realloc and free using the basic system calls brk and sbrk for heap.

2. A description of how this program works (i.e. its logic)

a) Malloc : I have used First fit algoritm to allocate the requested memory. I traverse the linked list to find the first block that can be used for allocation. If this block has extra memory so as to store metadata of a new block and one byte (only metadata is not be made, at least one byte should be there) then I fragment the block into two, one allocated and one residual block. However if no block is found then a new block is created at the tail of the linked list. If there is no memory available then brk system call is used to increase the limit and the code tries to use sbrk again to check if memory becomes available now.

b) Free: I traverse the linked list to find the linked list node that corresponds to the given pointer and make it available for allocation. If the block just above/below this block is free then the two blocks are coalesced into one.

c) Realloc : The pre-existing data is copied onto the stack and the heap pointer is freed. A new block with the new size is created and if successful the old data is copied back and new pointer is returned. If new block allocation fails then the old block is recreated and returned.

3. How to compile and run this program

Make sure that your test file includes the following headers

#include "mem.h"

Now run the following four commands

gcc -c mem.c

gcc -c mem_test.c

gcc -o mem_test mem_test.o mem.o

./mem_test
