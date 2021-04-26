/*
 * Name: Vedant Manawat
 * VNum: V00904582
 * April 13th 2021
 *
 * Skeleton code for CSC 360, Spring 2021,  Assignment #4
 *
 * Prepared by: Michael Zastre (University of Victoria) 2021
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

/*
 * Some compile-time constants.
 */

#define REPLACE_NONE 0
#define REPLACE_FIFO 1
#define REPLACE_LRU  2
#define REPLACE_SECONDCHANCE 3
#define REPLACE_OPTIMAL 4


#define TRUE 1
#define FALSE 0
#define PROGRESS_BAR_WIDTH 60
#define MAX_LINE_LEN 100


/*
 * Some function prototypes to keep the compiler happy.
 */
int setup(void);
int teardown(void);
int output_report(void);
long resolve_address(long, int);
void error_resolve_address(long, int);


/*
 * Variables used to keep track of the number of memory-system events
 * that are simulated.
 */
int page_faults = 0;
int mem_refs    = 0;
int swap_outs   = 0;
int swap_ins    = 0;
int prev_frame  = 0;


/*
 * Page-table information. You may want to modify this in order to
 * implement schemes such as SECONDCHANCE. However, you are not required
 * to do so.
 */
struct page_table_entry *page_table = NULL;
struct page_table_entry {
    long page_num;
    int dirty;
    int free;
    int clock_tick;
    int ref_bit;
};

/*
 * These global variables will be set in the main() function. The default
 * values here are non-sensical, but it is safer to zero out a variable
 * rather than trust to random data that might be stored in it -- this
 * helps with debugging (i.e., eliminates a possible source of randomness
 * in misbehaving programs).
 */

int size_of_frame = 0;  /* power of 2 */
int size_of_memory = 0; /* number of frames */
int page_replacement_scheme = REPLACE_NONE;


/*
    This function is reponsible for simulating the FIFO page replacement scheme. Its is only ever called if a new
    page is being referenced and it is not in the page table already. 
    
    When this scheme is being employed, it will keep a track of the "first in line" page so that when a new page is to be put
    on the table this, "first in line" page will be replaced. The global variable prev_frame allows to use such an approach. 

    Additionally, this function is also responsible to increment the swap_outs iff memwrite was TRUE. 
*/
void fifo_replacement(long page,int *prev_frame,int memwrite){
    for (int i=0; i<size_of_memory; i++){
        if(page_table[*prev_frame].dirty == TRUE){
            swap_outs++;
        }   

        if (memwrite == FALSE){
            page_table[*prev_frame].dirty = FALSE;
        }

        page_table[*prev_frame].page_num = page;
        *prev_frame = (*prev_frame+1)%size_of_memory;

        break;
    }
}

/*
    This function is used to help the LRU scheme determine which page has the smallest clock tick
    and updates the parameter of the function which is essentially the index of the frame that 
    needs to be replaced. 
*/
void findLRU(int *smallest){
    int i; 
    int min = page_table[0].clock_tick;
    *smallest = 0;

    for (i=0; i<size_of_memory; i++){
        if (min > page_table[i].clock_tick){
            min = page_table[i].clock_tick;
            *smallest = i;
        }
    }
}

/*
    This function is reponsible for simulating the LRU page replacement scheme. Its is only ever called if a new
    page is being referenced and it is not in the page table already. 
    
    When this scheme is being employed, it will keep a track of the page which was used first based on a system wide
    clock. So, when a new page is to be put on the table the page that will be replaced is going to be the page with the 
    lowest value of the system clock. In order to do this, a new attritube was added to the page table struct called "clock_tick".

    To find the smallest clock tick, this function calls another function: findLRU()

    Additionally, this function is also responsible to increment the swap_outs iff memwrite was TRUE. 
*/
void LRU_replacement(long page,int memwrite){
    int smallest = 0;
    for (int i=0; i<size_of_memory; i++){
        findLRU(&smallest); //find the index to change

        if(page_table[smallest].dirty == TRUE){
            swap_outs++;
        }

        if (memwrite == FALSE){
            page_table[smallest].dirty = FALSE;
        }

        page_table[smallest].page_num = page; //update the page num at that index
        page_table[smallest].clock_tick = mem_refs; //update its clock to current time
 
        break;
    }
}

/*
    This function is reponsible for simulating the Second Chance page replacement scheme. Its is only ever called if a new
    page is being referenced and it is not in the page table already. 
    
    This scheme is similar to the FIFO and so the gist of how this is implemented is the same. However, the only difference
    is the additional check that needs to be done to determine whether the page that is first in line has its reference bit 
    set to 1, if it does then we ignore this frame and choose the next first in line from the remaining frames. 
    This is to be done until a page with ref bit 0 is found and then replace the page at that frame with the new page. 

    Additionally, this function is also responsible to increment the swap_outs iff memwrite was TRUE. 
*/
void second_chance_replacement(long page,int memwrite,int *prev_frame){
    for (int i=0; i<size_of_memory; i++){
        if (page != page_table[i].page_num){
            if(page_table[*prev_frame].dirty == TRUE){
                swap_outs++;
            }

            if (memwrite == FALSE){
                page_table[*prev_frame].dirty = FALSE;
            }

            if (page_table[*prev_frame].ref_bit == TRUE){
                page_table[*prev_frame].ref_bit = FALSE;
                *prev_frame = (*prev_frame + 1)%size_of_memory;
                continue;
            }
        }
    }

    for (int j = 0; j<size_of_memory; j++){
        if (page_table[*prev_frame].ref_bit == FALSE){
            page_table[*prev_frame].page_num = page;
            page_table[*prev_frame].ref_bit = TRUE;
            *prev_frame = (*prev_frame + 1)%size_of_memory;
            break;
        }
    }
}

/*
 * Function to convert a logical address into its corresponding 
 * physical address. The value returned by this function is the
 * physical address (or -1 if no physical address can exist for
 * the logical address given the current page-allocation state.
 */

/*
    Only a few changes were added to this function and they are:
    - Updating the page clock_tick (for LRU). 
    - Setting the ref_bit to 1 (for second chance). 
    - Setting the dirty bit to TRUE if memwrite was TRUE. 
    - If a free frame is not found then call the correct replacement scheme based on what command the 
      user runs. 
*/
long resolve_address(long logical, int memwrite){
    int i;
    long page, frame;
    long offset;
    long mask = 0;
    long effective;

    /* Get the page and offset */
    page = (logical >> size_of_frame);

    for (i=0; i<size_of_frame; i++) {
        mask = mask << 1;
        mask |= 1;
    }
    offset = logical & mask;

    /* Find page in the inverted page table. */
    frame = -1;
    for ( i = 0; i < size_of_memory; i++) {
        if (!page_table[i].free && page_table[i].page_num == page) {
            frame = i;
            page_table[i].clock_tick = mem_refs;
            page_table[i].ref_bit = TRUE;

            if (memwrite == TRUE){
                page_table[i].dirty = TRUE;
            }

            break;
        }
    }


    /* If frame is not -1, then we can successfully resolve the
     * address and return the result. */
    if (frame != -1) {
        effective = (frame << size_of_frame) | offset;
        return effective;
    }

    /* If we reach this point, there was a page fault. Find
     * a free frame. */
    page_faults++;
    swap_ins++;

    for ( i = 0; i < size_of_memory; i++) {
        if (page_table[i].free) {
            frame = i;
            break;
        }
    }

    /* If we found a free frame, then patch up the
     * page table entry and compute the effective
     * address. Otherwise return -1.
     */
    if (frame != -1) {
        page_table[frame].page_num = page;
        page_table[i].free = FALSE;
        page_table[frame].clock_tick = mem_refs;
        page_table[frame].ref_bit = TRUE;
        
        if (memwrite == TRUE){
            page_table[frame].dirty = TRUE;
        }
        
        effective = (frame << size_of_frame) | offset;
        return effective;
    } else {
        if (page_replacement_scheme == 1){
            fifo_replacement(page,&prev_frame,memwrite); 
        }else if (page_replacement_scheme == 2){
            LRU_replacement(page,memwrite);
        }else if (page_replacement_scheme == 3){
            second_chance_replacement(page,memwrite,&prev_frame);
        }
        return 1;
    }
}

/*
 * Super-simple progress bar.
 */
void display_progress(int percent)
{
    int to_date = PROGRESS_BAR_WIDTH * percent / 100;
    static int last_to_date = 0;
    int i;

    if (last_to_date < to_date) {
        last_to_date = to_date;
    } else {
        return;
    }

    printf("Progress [");
    for (i=0; i<to_date; i++) {
        printf(".");
    }
    for (; i<PROGRESS_BAR_WIDTH; i++) {
        printf(" ");
    }
    printf("] %3d%%", percent);
    printf("\r");
    fflush(stdout);
}


int setup()
{
    int i;

    page_table = (struct page_table_entry *)malloc(
        sizeof(struct page_table_entry) * size_of_memory
    );

    if (page_table == NULL) {
        fprintf(stderr,
            "Simulator error: cannot allocate memory for page table.\n");
        exit(1);
    }

    for (i=0; i<size_of_memory; i++) {
        page_table[i].free = TRUE;
    }

    return -1;
}


int teardown()
{

    return -1;
}


void error_resolve_address(long a, int l)
{
    fprintf(stderr, "\n");
    fprintf(stderr, 
        "Simulator error: cannot resolve address 0x%lx at line %d\n",
        a, l
    );
    exit(1);
}


int output_report()
{
    printf("\n");
    printf("Memory references: %d\n", mem_refs);
    printf("Page faults: %d\n", page_faults);
    printf("Swap ins: %d\n", swap_ins);
    printf("Swap outs: %d\n", swap_outs);

    return -1;
}


int main(int argc, char **argv)
{
    /* For working with command-line arguments. */
    int i;
    char *s;

    /* For working with input file. */
    FILE *infile = NULL;
    char *infile_name = NULL;
    struct stat infile_stat;
    int  line_num = 0;
    int infile_size = 0;

    /* For processing each individual line in the input file. */
    char buffer[MAX_LINE_LEN];
    long addr;
    char addr_type;
    int  is_write;

    /* For making visible the work being done by the simulator. */
    int show_progress = FALSE;

    /* Process the command-line parameters. Note that the
     * REPLACE_OPTIMAL scheme is not required for A#3.
     */
    for (i=1; i < argc; i++) {
        if (strncmp(argv[i], "--replace=", 9) == 0) {
            s = strstr(argv[i], "=") + 1;
            if (strcmp(s, "fifo") == 0) {
                page_replacement_scheme = REPLACE_FIFO;
            } else if (strcmp(s, "lru") == 0) {
                page_replacement_scheme = REPLACE_LRU;
            } else if (strcmp(s, "secondchance") == 0) {
                page_replacement_scheme = REPLACE_SECONDCHANCE;
            } else if (strcmp(s, "optimal") == 0) {
                page_replacement_scheme = REPLACE_OPTIMAL;
            } else {
                page_replacement_scheme = REPLACE_NONE;
            }
        } else if (strncmp(argv[i], "--file=", 7) == 0) {
            infile_name = strstr(argv[i], "=") + 1;
        } else if (strncmp(argv[i], "--framesize=", 12) == 0) {
            s = strstr(argv[i], "=") + 1;
            size_of_frame = atoi(s);
        } else if (strncmp(argv[i], "--numframes=", 12) == 0) {
            s = strstr(argv[i], "=") + 1;
            size_of_memory = atoi(s);
        } else if (strcmp(argv[i], "--progress") == 0) {
            show_progress = TRUE;
        }
    }

    if (infile_name == NULL) {
        infile = stdin;
    } else if (stat(infile_name, &infile_stat) == 0) {
        infile_size = (int)(infile_stat.st_size);
        /* If this fails, infile will be null */
        infile = fopen(infile_name, "r");  
    }


    if (page_replacement_scheme == REPLACE_NONE ||
        size_of_frame <= 0 ||
        size_of_memory <= 0 ||
        infile == NULL)
    {
        fprintf(stderr, 
            "usage: %s --framesize=<m> --numframes=<n>", argv[0]);
        fprintf(stderr, 
            " --replace={fifo|lru|optimal} [--file=<filename>]\n");
        exit(1);
    }


    setup();

    while (fgets(buffer, MAX_LINE_LEN-1, infile)) {
        line_num++;
        if (strstr(buffer, ":")) {
            sscanf(buffer, "%c: %lx", &addr_type, &addr);
            if (addr_type == 'W') {
                is_write = TRUE;
            } else {
                is_write = FALSE;
            }

            if (resolve_address(addr, is_write) == -1) {
                error_resolve_address(addr, line_num);
            }
            mem_refs++;
        } 

        if (show_progress) {
            display_progress(ftell(infile) * 100 / infile_size);
        }
    }
    

    teardown();
    output_report();

    fclose(infile);

    exit(0);
}
