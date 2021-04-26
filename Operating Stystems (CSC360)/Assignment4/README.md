# Name: Vedant Manawat
# VNumber: V00904582
# CSC 360 Assignment 4
# April 13th 2021 

## This README file describes the tasks I have completed to implement the page replacement schemes.

## First In First Out (FIFO):
* This task required us to implement the FIFO replacement scheme, which is, when a page has been added to the table we keep a track of who the first arriving page was. 
* When the table is full and a new page is referenced (i.e. a page fault), we must decide which page needs to be replaced and this is where the first arriving page is replaced. 
* My implementation:
    * The most general form would be to use a queue as it uses a FIFO scheme. However, I did not use a queue and instead did as follows:
        1. Create a global variable that would cycle through the frames (0,size_of_memory-1) constantly, this was my way to simulate a queue.
        2. If the page being referenced is in that frame we do nothing and just break out of the function and reference the next page.
        3. If the page being referenced is not in the table then we use this global variable to determine who the first arriving page was and replace the page at the index and increment the variable to point to the next arriving page. 


## Least Recently Used (LRU):
* This task required us to implement the LRU replacement scheme, which is, when a page has been added to the table we keep a track of what "time" it arrived. 
* When the table is full and a new page is referenced (i.e. a page fault), we must decide which page need to be replaced and this is done based on which pages "clock-tick" was the earliest (lowest).
* My implementation:
    1. I implemented this by adding an attribute to the page_table struct called a clock_tick, this is essentially the clock counter for each page is constantly updated based on the number of memory references that have been made. 
    2. When initially filling the table the mem_ref counter is copied to the clock_tick of the page being referenced. 
    3. When a page fault occurs and a new page needs to be added, the following happens:
        - If that page already exists in the table, then update its clock_tick to the current mem_ref number and move on. 
        - If that page is not in the table, then, run through the table to determine who has the smallest clock_tick and get its index, and replace the page at the index from the table. Note, that when this is done, we must, update the clock_tick of the new added page to the current mem_ref number. 

## Second Chance:
* This task required us to implement the Second Chance replacement scheme, which is, when a page has been added to the table we set the pages' reference bit to 1, to indicate that can be given another chance to have control of the CPU.
* This bit must be set to 0 if a new page which is not in the table has been referenced. 
* My implementation:
    1. I implemented this by adding an attribute to the page_table struct called a ref_bit. 
    2. Everytime a page is referenced and put onto the table its ref_bit is set to 1. 
    3. If a page is referenced and it is not in the table, then we run through the table and do the following:
        - We check who the first arriving page is (as second chance is a variation of FIFO), if the ref_bit of the page at the given frame is 1 then we set it back to 0, indicating that it has been given a second chance. 
        - If the bit is 0 of that page then we replace that page with the newly referenced page and set its ref_bit to 1. 
    4. **Note that the way I decide which page needs to be replaced is the same as my FIFO implementation with the additional check of the reference bit.**


## *Files provided are as follows:* 
* virtmem.c
* README.md
