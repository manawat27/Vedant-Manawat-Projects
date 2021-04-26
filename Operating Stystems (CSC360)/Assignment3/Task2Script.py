# Name: Vedant Manawat
# VNumber: V00904582
# CSC 360 Assignment 3 Task 2
# March 25th 2021 

import subprocess
import os
import re
import random
import matplotlib.pyplot as pyplot
import numpy as np


"""
Defining some global variables
"""
data_list = []
seeds = []
average_wait = []
average_ta = []

"""
This function creates the command that will be used to run the simulaton. 
Parameters: random seed, quantum length and dispatch length to create this command
Return Value: Piped comamnd to simulate (e.g. ./simgen 1000 1393 | ./rrsim --quantum 500 --dispatch 25 > out.txt)
"""
def create_command(seed,qlen,dlen):
    simgen_pip_cmd = "./simgen 1000 " + str(seed) + " | ./rrsim --quantum " + str(qlen) + " --dispatch " + str(dlen) + " > out.txt"
    return simgen_pip_cmd

"""
This function will parse the data written in out.txt after each run of the simulator
It will add to a list all lines that represent a task exiting. 
"""
def parse_outfile():
    f = open("out.txt","r")
    for x in f:
        if "EXIT" in x:
            data_list.append(x)



""" 
Credit for some of the code in this function goes to the following:
    - https://stackoverflow.com/questions/12572362/how-to-get-a-string-after-a-specific-substring
    - https://stackoverflow.com/questions/4666973/how-to-extract-the-substring-between-two-markers

This function will parse through the data_list and calculat the average wait time and average turnaround time
of the 20 simulations for each quantum dispatch pair (480 simulations in total). It will then append this average
to a corresponding lists. 
"""
def get_average():
    total_wait = 0
    total_ta = 0
    avg_wait = 0
    avg_ta = 0

    i=0
    for item in data_list:
        wait = re.search("w=(.+?) ta",item).group(1)
        ta = item.split("ta=",1)[1]
        total_wait = total_wait + float(wait)
        total_ta += float(ta)
        i += 1

    avg_wait = total_wait/i
    avg_ta = total_ta/i

    average_wait.append(avg_wait)
    average_ta.append(avg_ta)

"""
Parameters: quantum length and dispatch length 
This function is reponsible for recursively executing the commands that have been created by another function. 
This function calls the function that creates the command and parses the file out.txt. It also calls the function to
calculate the averages. 
"""
def run_sims(qlen,dlen):
    for item in seeds:
        seed = item
        command = create_command(seed,qlen,dlen)
        print(command)
        os.system(command)
        parse_outfile()

    get_average()
    data_list.clear()

    dlen = dlen + 5
    if(dlen <= 25):
        print("Changing qlen and dlen to: " + str(qlen) + " and " + str(dlen) + " respectively")
        run_sims(qlen,dlen)
    else:
        dlen = 0
        qlen = qlen + 50
        if (qlen == 100):
            print("Changing qlen and dlen to: " + str(qlen) + " and " + str(dlen) + " respectively")
            run_sims(qlen,dlen)
        elif (qlen == 150):
            qlen = qlen + 100
            print("Changing qlen and dlen to: " + str(qlen) + " and " + str(dlen) + " respectively")
            run_sims(qlen,dlen)
        elif (qlen == 300):
            qlen = qlen + 200
            print("Changing qlen and dlen to: " + str(qlen) + " and " + str(dlen) + " respectively")
            run_sims(qlen,dlen)
        if qlen > 500:
            return

"""
Credit for some of the code in this function goes to the following:
    - https://www.w3resource.com/graphics/matplotlib/basic/matplotlib-basic-exercise-5.php
    - https://stackoverflow.com/questions/8920436/matplotlib-how-to-start-ticks-leaving-space-from-the-axis-origin
    - https://stackoverflow.com/questions/9433258/markers-on-plot-edges-cut-off-in-matplotlib
    - 

This function is responsible for grabbing the averages and plotting them in their respective graphs. 
It will create two graphs, one for average wait time and one for average turnaround time and save them as a PDF. 
"""
def plot_graphs():

    ################### PLOTTING WAIT TIME GRAPH HERE ###################
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    x = np.array([0,5,10,15,20,25])
    wait_y1 = np.array(average_wait[0:6])

    wait_y2 = np.array(average_wait[6:12])
    wait_y3 = np.array(average_wait[12:18])
    wait_y4 = np.array(average_wait[18:24])

    pyplot.plot(x,wait_y1,label="q=50",marker='+',color="purple",markersize=10,clip_on=False)
    pyplot.plot(x,wait_y2,label="q=100",marker="x",color="green",markersize=10,clip_on=False)
    pyplot.plot(x,wait_y3,label="q=250",marker="2",markersize=10,clip_on=False)
    pyplot.plot(x,wait_y4,label="q=500",marker="s",color="orange",markerfacecolor="none",markersize=10,clip_on=False)

    pyplot.xlabel("Dispatch Overhead")
    pyplot.ylabel("Averga waiting time")
    pyplot.title("Round Robin scheduler -- # tasks: 1000;seed value: variable seed value")

    pyplot.legend()
    ax.set_xlim(0,max(x))
    pyplot.savefig('Wait_Time.pdf')

    ############################### PLOTTING TURNAROUND TIME GRAPH HERE ###############################
    fig2 = pyplot.figure()
    ax2 = fig2.add_subplot(1,1,1)
    x = np.array([0,5,10,15,20,25])
    ta_y1 = np.array(average_ta[0:6])

    ta_y2 = np.array(average_ta[6:12])
    ta_y3 = np.array(average_ta[12:18])
    ta_y4 = np.array(average_ta[18:24])

    pyplot.plot(x,ta_y1,label="q=50",marker='+',color="purple",markersize=10,clip_on=False)
    pyplot.plot(x,ta_y2,label="q=100",marker="x",color="green",markersize=10,clip_on=False)
    pyplot.plot(x,ta_y3,label="q=250",marker="2",markersize=10,clip_on=False)
    pyplot.plot(x,ta_y4,label="q=500",marker="s",color="orange",markerfacecolor="none",markersize=10,clip_on=False)

    pyplot.xlabel("Dispatch Overhead")
    pyplot.ylabel("Averga turnaround time")
    pyplot.title("Round Robin scheduler -- # tasks: 1000;seed value: variable seed value")

    pyplot.legend()
    ax2.set_xlim(0,max(x))
    pyplot.savefig('Turnaround_Time.pdf')

"""
The main function which calls make to compile the C code. It also generates 20 random seeds and appends it to a list. 
This function initally sets the qlen and dlen and then calls the run_sims() function and the plot_graphs() function. 
"""
def main():
    qlen = 50
    dlen = 0
    subprocess.call(["make"])
    for i in range (0,20):
        seed = random.randint(0,9999)
        seeds.append(seed)
    run_sims(qlen,dlen)
    plot_graphs()

if __name__ == "__main__":
    main()