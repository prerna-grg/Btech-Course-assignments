import math
import numpy as np

# takes input page number page offset frame number frame offset and page fault status and prints to console
def printData( pn , po , fn , fo , pf ):
	print('Page Number: ' + str(pn)+" "+'Page Offset: ' + str(po))
	print('Frame Number: ' + str(fn)+" "+'Frame Offset: ' + str(fo))
	print("Page Fault: "+pf)
	print()
	
# simulation function
def simulate(virtual_address_size, page_size, ram_size, page_rep_algo, ref_addresses):
	offset_bits = int(math.log2(page_size)) + 10 
	page_num_bits = virtual_address_size - offset_bits
	frame_size = page_size
	num_frames = int((ram_size*1024*1024)/(frame_size*1024))
	
	# initially all entries are invalid i.e. the entire table is empty
	page_table = [-1 for i in range(num_frames)]
	
	# initialise all frequencies to zero
	access_freq = [0 for i in range(num_frames)]
	
	page_index = 0
	misses = 0
	
	# traverse the sequence of addresses
	for addr in ref_addresses:
		# find the page number
		page_number = addr >> offset_bits
		# find the offset
		page_offset = ((2**offset_bits)-1) & addr
		frame_offset = page_offset
		
		
		while True:
			page_fault = 'yes'
			# find if the page number exists in the page table
			if page_number in page_table:			
				# calculate the corresponding frame number
				frame_number = page_table.index(page_number) 
				# update the frequency of access of this page
				access_freq[ frame_number ] += 1
				page_fault = 'no'
				break
				
			# page was not found in the page table
			misses += 1
		
			# if empty frame available it will be added here
			# for FIFO replacement will occur here itself (except when the current index is last)
			if page_index<len(page_table):
				page_table[page_index] = page_number # store the new page number
				access_freq[page_index] = 1 # initialise the access frequency by 1
				frame_number = page_index # calculate the frame number
				page_index += 1 # update the index for the next inserted page 
				break
		
			# FIFO ( for the last page index we replace by the first frame and continue from there )
			if(page_rep_algo.upper()=='FIFO'):
				frame_number = 0
				page_table[0] = page_number # store the new page number
				access_freq[0] = 1 # initialise the access frequency by 1
				page_index = 1  # initialise the page index for the next page by 1
				break
			
			# LFU
			if(page_rep_algo.upper()=='LFU'):
				frame_number = access_freq.index( min(access_freq) ) # find the frame with minimum frequency
				page_table[frame_number] = page_number # store the new page there
				access_freq[frame_number] = 1 # initialise the access frequency by 1
				break

			# MFU
			if(page_rep_algo.upper()=='MFU'):
				frame_number = access_freq.index( max(access_freq) ) # find the frame with maximum frequency
				page_table[frame_number] = page_number # store the new page there
				access_freq[frame_number] = 1 # initialise the access frequency by 1
				break				
		#printData(page_number , page_offset , frame_number , str(frame_offset) , page_fault)
	
	# return the total percentage of misses
	return "%Rate of Page Faults = " + str(100.0*float(misses)/len(ref_addresses)) + "%\n"

