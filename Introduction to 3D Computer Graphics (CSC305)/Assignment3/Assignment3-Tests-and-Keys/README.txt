Name: Vedant Manawat
VNumber: V00904582

April 14th 2021

CSC 305 Assignment 3

This is the README file for the corresponding assignment submission. This file containts a list of objectives accomplished/not accomplished by me in order to complete the assignment.

Run the code with the following command:
    python3 RayTracer.py -filename.txt-
    instead of "filename.txt" add the actual file to be parsed and outputted. 

Tasks Completed:
    - File parsing.
    - Calculating intersections and returning the correct R G B values to write to the ppm file. 
    - Writing to the ppm (ppm6) file correctly. 
    - Ambient lighting. 
    - Diffuse lighting. 
    - Specular lighting. 

Task Omitted:
    - Shadows
    - Reflection (attempted to do reflection, however, didn't have enough time to fully crack it). 

It is important to note that my implementation is a single threaded implementation and consequently it takes upto a minute to finish running and produce an output. If I had more time then I would have made it a multithreaded program in order to reduce the time taken by the program.
It is also important to note that some of the outputs won't match the key, I suspect the reason for this is due to the way I'm writing to the ppm file, for some reason the output generated by me seems to be situated in such a way that the back of the scene is shown rather than the front. 
