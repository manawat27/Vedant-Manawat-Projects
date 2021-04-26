/* 
    Name: Vedant Manawat
    VNumber: V00904582

    CSC 360 Assignment 3 Task 1
    March 25th 2021 
*/

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "linkedlist.h"

#define MAX_BUFFER_LEN 80

taskval_t *event_list = NULL;

void print_task(taskval_t *t, void *arg,int tick) {
    printf("[%05d] id=%05d req=%0.2f used=%0.2f\n",
        tick,
        t->id,
        t->cpu_request,
        t->cpu_used
    );  
}


void increment_count(taskval_t *t, void *arg) {
    int *ip;
    ip = (int *)arg;
    (*ip)++;
}

/* 
    This is the function that is responsible for running the simulation of Round Robin CPU scheduling

    This function takes are parameters qlen (quantum) and dlen (dispatch lenght).

    At every tick the function checks if something in the current (copy of event_list) has arrived to be run.
    If so, add it to the read_q and simulate its dispatch and execution. If it demands more CPU then append it to the back
    of the ready_q. 

    If no new task is in the ready_q then the CPU will simply IDLE. 
*/
void run_simulation(int qlen, int dlen) {
    taskval_t *ready_q = NULL;
    taskval_t *current = event_list;
    taskval_t *temp = NULL;
    int tick = 0;

    while(current != NULL){
        if (tick < current->arrival_time){
            printf("[%05d] IDLE\n",tick);
            tick++;
        }else{
            temp = current;
            current = remove_front(current);
            ready_q = add_end(ready_q,temp);

            while(ready_q != NULL){
                if (dlen == 0){
                    printf("[%05d] DISPATCHING\n",tick);
                }else{
                    for (int i=0; i<dlen; i++){
                        printf("[%05d] DISPATCHING\n",tick);
                        tick++;
                        if (current != NULL && tick == current->arrival_time){ 
                            temp = current;
                            current = remove_front(current);
                            ready_q = add_end(ready_q,temp);
                        }
                    }
                }

                for (int j=0; j<qlen; j++){
                    print_task(ready_q,NULL,tick);
                    ready_q->cpu_used++;
                    tick++;

                    if (current != NULL && tick == current->arrival_time){
                        temp = current;
                        current = remove_front(current);
                        ready_q = add_end(ready_q,temp);
                    }

                    if (ready_q->cpu_used >= ready_q->cpu_request){
                        ready_q->wait_time = tick - ready_q->arrival_time - ready_q->cpu_request;
                        double ta = tick - ready_q->arrival_time;
                        printf("[%05d] id=%05d EXIT w=%0.2f ta=%0.2f\n",tick,ready_q->id,ready_q->wait_time,ta);
                        ready_q = remove_front(ready_q);
                        j=qlen;
                    }
                }
                
                if (ready_q != NULL && ready_q->cpu_request > qlen){
                    temp = ready_q;
                    ready_q = remove_front(ready_q);
                    ready_q = add_end(ready_q,temp);
                }

                if (ready_q == NULL){
                    exit(0);
                }

            }
        }
    }
}

int main(int argc, char *argv[]) {
    char   input_line[MAX_BUFFER_LEN];
    int    i;
    int    task_num;
    int    task_arrival;
    float  task_cpu;
    int    quantum_length = -1;
    int    dispatch_length = -1;

    taskval_t *temp_task;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--quantum") == 0 && i+1 < argc) {
            quantum_length = atoi(argv[i+1]);
        }
        else if (strcmp(argv[i], "--dispatch") == 0 && i+1 < argc) {
            dispatch_length = atoi(argv[i+1]);
        }
    }

    if (quantum_length == -1 || dispatch_length == -1) {
        fprintf(stderr, 
            "usage: %s --quantum <num> --dispatch <num>\n",
            argv[0]);
        exit(1);
    }


    while(fgets(input_line, MAX_BUFFER_LEN, stdin)) {
        sscanf(input_line, "%d %d %f", &task_num, &task_arrival,
            &task_cpu);
        temp_task = new_task();
        temp_task->id = task_num;
        temp_task->arrival_time = task_arrival;
        temp_task->cpu_request = task_cpu;
        temp_task->cpu_used = 0.0;
        temp_task->wait_time = 0.0;
        temp_task->clock_tick = 0;
        event_list = add_end(event_list, temp_task);
    }

#ifdef DEBUG
    int num_events;
    apply(event_list, increment_count, &num_events);
    printf("DEBUG: # of events read into list -- %d\n", num_events);
    printf("DEBUG: value of quantum length -- %d\n", quantum_length);
    printf("DEBUG: value of dispatch length -- %d\n", dispatch_length);
#endif

    run_simulation(quantum_length, dispatch_length);

    return (0);
}