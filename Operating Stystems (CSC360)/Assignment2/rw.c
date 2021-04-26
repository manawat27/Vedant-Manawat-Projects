/*
    Vedant Manawat
    V00904582
    March 10th 2021
    CSC 360 Assignment 2 Task 1: Readers and Writers
*/

/*Required Headers*/

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <semaphore.h>
#include "rw.h"
#include "resource.h"

/*
 * Declarations for reader-writer shared variables -- plus concurrency-control
 * variables -- must START here.
 */

static resource_t data;

sem_t writer;
sem_t reader;
int read_counter;


// The purpose of this function is to initialize the two semaphores, the resource and the counter
void initialize_readers_writer() {
    /*
     * Initialize the shared structures, including those used for
     * synchronization.
     */
    read_counter = 0;
    sem_init(&writer,0,1);
    sem_init(&reader,0,1);
    init_resource(&data, " ");
}

// Basic concept of the functions below are inspired by the following video:
// https://www.youtube.com/watch?v=e69goh-_Ve0&ab_channel=Education4u 
// https://stackoverflow.com/questions/58083898/readers-writers-problem-in-c-using-pthreads-and-semaphores


// The purpose of this function is to ensure that whenever it is called the thread will trigger a read operation,
// when this happens the reader will lock the semaphore and proceed to read to the resource.
// If there is a writer then the writer will be told to wait for the reader to read first
// Once the operation is completed, another reader can enter (multiple readers can enter and read at the same time).
void rw_read(char *value, int len) {
    sem_wait(&reader);
    read_counter++;

    if (read_counter == 1){
        sem_wait(&writer);
    }

    sem_post(&reader);
    read_resource(&data,value,len);
    sem_wait(&reader);
    read_counter--;

    if (read_counter == 0){
        sem_post(&writer);
    }
    sem_post(&reader);
}

// The purpose of this function is to ensure that whenever it is called the thread will trigger a write operation,
// when this happens the writer will lock the semaphore and proceed to write to the resource.
// Once the operation is completed, another writer can enter. 
void rw_write(char *value, int len) {

    sem_wait(&writer);
    write_resource(&data,value,len);
    sem_post(&writer);
}
