Name: Vedant Manawat
VNumber: V00904582

March 10th, 2021
CSC 360 Assignment 2

This README file describes the tasks I have completed for of the two tasks as mentioned in the assignment PDF.

Task 1: Readers and Writer

- This task required us to implement the code for a simple readers and writers problem.
- The problem on a very basic is level is such:
    - When a thread is created it can either read from the resource or write to the resource. 
- Our job is to write code such that the readers have priority, this means that if there a reader waiting to read the resource and a writer has arrived to write to it then we want the reader to read it first before the writer can update the value of the resource. 
- My implementation uses two semaphores, a variable of type resource_t and a counter.


Task 2: Reusable Barriers (for MEETUP):

- This task required us to implement the code for a made up scenario as such:
    - A group of n people gather and either the first person in the group shares its value (codeword) with the rest of the group at which point the group can disperse.
    - Or the nth person shares this value with the rest of the group, at which point the group can disperse. 
- My implementation works in two ways:
    1. If the meetup is of type MEET_FIRST then the first person to arrive in a group of n will write to the resource and wait for the other n-1 peple to arrive. When these n-1 arrive they each read the value from the resource and are ready to disperse. Only when all members of a group have arrived can they leave. My code allows for members from different groups be waiting at the same time, however, it doesn't overwrite the codeword before a group has had a chance to read it. 
    
    2. If the meetup is of type MEET_LAst then the last person to arrive in a group of n will write to the resource. When the members arrive from first to last, they will wait until the nth member is here and then read the value that this person has written in the codeword. Only when all memebrs of a group have read the codeword can they leave and another group will be allowded into the queue. 

IMPORTANT NOTE: I WAS SUCCESSFULLY ABLE TO IMPLEMENT MEET_FIRST, HOWEVER, FOR MEET_LAST I WAS ABLE TO IDENTIFY WHICH THREAD BELONGED TO WHICH GENERATION AND WHAT THE CODEWORD SHOULD BE (WAS ABLE TO WRITE CORRECTLY) BUT I WAS NOT ABLE TO READ THE VALUE PROPERLY, HENCE MAKING THE IMPLEMENTATION OF MEET_LAST INCOMPLETE. 


Files Submitted: Files 1-5 are required as per the assignment PDF, file 6 has been added just in case it is needed during evaluation 
1. rw.c
2. rw.h
3. meetup.c
4. meetup.h
5. README.md
6. network.h
