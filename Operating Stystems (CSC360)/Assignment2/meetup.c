/*
    Vedant Manawat
    V00904582
    March 10th 2021
    CSC 360 Assignment 2 Task 2: Boba Fett Meetup
*/


/*Required Headers*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <semaphore.h>
#include "meetup.h"
#include "resource.h"

/*
 * Declarations for barrier shared variables -- plus concurrency-control
 * variables -- must START here.
 */

int count;
int num_threads;
pthread_mutex_t my_mutex;
pthread_cond_t meetlast_barrier;
pthread_cond_t my_barrier;
int generation; 
int person_counter;


int codeword_provider;
static resource_t codeword;


// The purpose of this function is to initialize the two mutexes, two cond_vars, the resource
// the counter and generation and an intermediate counter
void initialize_meetup(int n, int mf) {
    char label[100];
    int i;
    count = 0;
    generation = 0;
    person_counter = 0;

    num_threads = n;
    codeword_provider = mf;

    init_resource(&codeword, "");

    if (n < 1) {
        fprintf(stderr, "Who are you kidding?\n");
        fprintf(stderr, "A meetup size of %d??\n", n);
        exit(1);
    }

    /*
     * Initialize the shared structures, including those used for
     * synchronization.
     */
    int mutex_status = pthread_mutex_init(&my_mutex, NULL);
    if (mutex_status != 0){
        fprintf(stderr, "Could not initialize 'mutex'\n");
        exit(1);
    }

    int barrier_status = pthread_cond_init(&my_barrier,NULL);
    if (barrier_status != 0){
        fprintf(stderr, "Could not initialize 'barrier'\n");
        exit(1);
    }

    int meetlast_barrier_status = pthread_cond_init(&meetlast_barrier,NULL);
    if (meetlast_barrier_status != 0){
        fprintf(stderr, "Could not initialize 'barrier'\n");
        exit(1);
    }
}


//Credit for the following code: The following code is based/built upon the pseudocode shown in class
// Specifically, this code can be found on slide number 73 of slide set 5: Synchronization 

// This function has two purposes:
//  1. If the meetup is of type MEET_FIRST it will let the first thread to enter write to the codeword and wait until
//      the rest of it group members come and read the codeword. 
//  2. If the meetup is of type MEET_LAST it will tell all incoming threads from a group of n to wait for the last thread
//      to come and write to the resource and only then the ones waiting can read the resource.
void join_meetup(char *value, int len) {

    // Implementation of MEET_FIRST begins here
    if(codeword_provider == MEET_FIRST){
        pthread_mutex_lock(&my_mutex);
        count = count + 1;
        if (count < num_threads){
            if (person_counter == 0){
                int my_generation = generation;
                while (my_generation == generation){
                    write_resource(&codeword,value,len);
                    person_counter = person_counter + 1;
                    pthread_cond_wait(&my_barrier,&my_mutex);
                }
            }else if (person_counter > 0){
                read_resource(&codeword,value,len);
                person_counter = person_counter + 1;
                pthread_cond_wait(&my_barrier,&my_mutex);
            }
        }else{
            int prev_count = count;
            int prev_generation = generation;
            count = 0;
            person_counter = 0;
            generation++;
            pthread_cond_broadcast(&my_barrier);
            read_resource(&codeword,value,len);
        }
        pthread_mutex_unlock(&my_mutex);

    // Implementation of MEET_LAST begins here
    }else if(codeword_provider == MEET_LAST){
        char temp_codeword[len];
        pthread_mutex_lock(&my_mutex);
        count = count + 1;
        if (count < num_threads){
            int my_generation = generation;
            while (my_generation == generation){
                pthread_cond_wait(&meetlast_barrier,&my_mutex);

                pthread_cond_wait(&my_barrier,&my_mutex);
                read_resource(&codeword,value,len);

                pthread_cond_broadcast(&meetlast_barrier);
            }
        }else{
            int prev_generation = generation;
            count = 0;
            generation++;
            
            write_resource(&codeword,value,len);
            strncpy(temp_codeword,value,len);

            pthread_cond_broadcast(&my_barrier);
        }
        pthread_mutex_unlock(&my_mutex);
    }
}
