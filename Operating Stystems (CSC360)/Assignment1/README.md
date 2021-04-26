Name: Vedant Manawat
VNumber: V00904582

Feb. 12 2021
CSC 360 Assignment 1

This README file describes the tasks I have completed for each of the four features described in the assignment pdf.

Feature a:
- The program is able to repeadtedly prompts the user for commands and executes those commands in child processes
- The prompt can be found in the first line of the .sh360rc file
- The .sh360rc also contains the the absolute paths of the directories

Feature b:
- If the user types exit the emulated shell will shutdown
- The program only accpets upto 7 arguments from the user

Feature c:
- If a command is preceeded with an OR then the program can redircet the output from stdout to a file specified after the "->"

Feature d:
- The program can pipe simple commands like ls | wc (PP ls -> wc)


It is important to note that my submission for this assignment does not meet all the requirements and due to time constraints I was not able to do the following:
- Simple error handling mentioned in the assignment specification
- Piping three commands
- Piping where each command can have multiple options
