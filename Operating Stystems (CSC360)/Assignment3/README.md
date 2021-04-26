# Name: Vedant Manawat
# VNumber: V00904582
# CSC 360 Assignment 3
# March 25th 2021 

## This README file describes the tasks I have completed for of the two tasks as mentioned in the assignment PDF.

## Task 1: rrsim.c:
* This task required us to implement a function that would simulate the way Round Robin CPU scheduling works.
* A basic overview of the way the program runs is as follows:
    * Each task runs turn by turn and gets given by the CPU an equal share of the time/quantum. 
* How my implementation works:
    1. First "copies" over the even_list just so I can keep track of what events need to be handled.
    2. Then, checks at every tick if a new task needs to be put onto the ready_q.
    3. If not, then print IDLE, else DISPATCH for dlen and then print the task for the qlen.
    4. *Note that even when a task in on the ready_q I will check if a new task needs to be added to the queue or not.*
    5. If a task has used up all of the quantum, I check two things:
        * Is the task ready to EXIT (ie, is cpu_used >= cpu_req), if so then remove it from the ready_q.
        * If the task is not ready to EXIT then shuffle it to the back of the queue, so that it can get CPU time again. 
        * *Note that if a new task arrives at the same time as one task EXITING/shuffling then I give priority to the task that is EXITING/shuffling and then add the new task behind it.*
    6. *I added a new attribute to each task called wait_time to help keep track of the wait_times of each task.*


## Task 2: Analyzing output from the simulator 
* This task required us to implement a script that would be responsible to compile and run the C program described in the task above. 
* We were required to run the simulation for 20 different seeds with different 24 combinations of qlen and dlen (480 runs in total).
* *This script will take some time to run as its simulating rrsim 480 times with a 1000 tasks. It should take upto 6 minutes.*
* How my implementation works:
    1. First compile the C program. 
    2. Generate 20 random seeds. 
    3. Call a function that runs recursively and is responsible for the following:
        * Generate the command that needs to be executed.
        * Execute the command, parse the output to get the data needed to get the averages. 
        * Calculate the averages and store it in two seperate lists
    4. Plot the two graphs mentioned below with the list of averages:
        * Graph1: Dispatch Cost vs Average Wait Time
        * Graph2: Dispatch Cost vs Average Turnaround Time


## *Files provided are as follows:* 
* rrsim.c
* linkedlist.c and linkedlist.h
* Task2Script.py 
* graph_waiting.pdf and graph_turnaround.pdf
* README.md


