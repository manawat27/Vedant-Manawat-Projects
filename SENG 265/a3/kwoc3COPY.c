//void print_word(node_t *node, void *arg)
//{
//    char *format = (char *)arg;
//    printf(format, node->text);
//}
//
//
//#ifdef DEBUG
//
///*
// * Just showing the use of the linked-list routines.
// */
//
//void _demo() {
//printf("DEBUG: in _demo\n");
//    char *words_german[] = {"Der", "Kater", "mit", "Hut."};
//    int   words_german_len = 4;
//
//    char *words_english[] = {"The", "cat", "in", "the", "hat."};
//    int   words_english_len = 5;
//
//    node_t *temp_node = NULL;
//    node_t *head = NULL;
//
//    int i;
//
//    /* Add the words in German, at the front. */
//    for (i = 0; i < words_german_len; i++) {
//        temp_node = new_node(words_german[i]);
//        head = add_front(head, temp_node);
//    }
//
//    /* Add the words in English, at the end. */
//    for (i = 0; i < words_english_len; i++) {
//        temp_node = new_node(words_english[i]);
//        head = add_end(head, temp_node);
//    }
//
//    /* Print the list of words. */
//
//    apply(head, print_word, "--> %s\n");
//
//    /* Free up the memory. This is done rather deliberately
//     * and manually.  Asserts are liberally used here as they
//     * express state that *must* be true if all of the code is
//     * correctly working.
//     */
//
//    temp_node = head;
//    while (temp_node != NULL) {
//        assert(temp_node != NULL);
//        head = remove_front(head);
//        free(temp_node);
//        temp_node = head;
//    }
//
//    assert(head == NULL);
//}
//
//#endif

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "emalloc.h"
#include "listy.h"
#include <ctype.h>

#define MAX_LINE_LEN 100
#define MAX_WORD_LEN 40
#define MAX_WORDS_PER_LINE

typedef struct Lines_and_Words Lines_and_Words;
struct Lines_and_Words{
	char array_lines[MAX_LINE_LEN];
};

struct Ntab{
	Lines_and_Words *lines;
	int max_elements;
	int index;
};

enum{
	NINIT = 8,
	NGROW = 2
};

void command_line_input(int argc, char *argv[], char **input_file, char **exp_filename);
void read_file_in_array(char *filename, struct Ntab *ntab);
int add_line(char *line, struct Ntab *ntab);
void store_words(struct Ntab *ntab, node_t **words, int *word_counter);
void remove_exceptions(node_t **words, node_t **exp_words, int *word_counter);
node_t *remove_word(node_t *words, char *text);
void sort(node_t **words, int word_counter);
int compare(const void *a, const void *b);
void remove_duplicates(node_t **words, int *word_counter);
void print_output(node_t **words, struct Ntab *ntab_lines, int word_counter);
int longest_word(node_t **words);
int count_words_in_line(char word[MAX_WORD_LEN], char buffer[MAX_LINE_LEN]);


int main(int argc, char *argv[]){
	char *filename = NULL;
	struct Ntab ntab_lines;
	ntab_lines.lines = NULL;
	ntab_lines.max_elements = 0;
	ntab_lines.index = 0;
	node_t *words = NULL;
	int word_counter = 0;
	
	char *exp_filename = NULL;
	struct Ntab ntab_exp_lines;
	ntab_exp_lines.lines = NULL;
	ntab_lines.max_elements = 0;
	ntab_lines.index = 0;
	node_t *exp_words = NULL;
	int exp_word_counter = 0;
	
	command_line_input(argc, argv, &filename, &exp_filename);
	
	read_file_in_array(filename, &ntab_lines);
	store_words(&ntab_lines, &words, &word_counter);
	
	read_file_in_array(exp_filename, &ntab_exp_lines);
	store_words(&ntab_exp_lines, &exp_words, &exp_word_counter);
	remove_exceptions(&words, &exp_words, &word_counter);
	
	print_output(&words, &ntab_lines, word_counter);
	
#ifdef DEBUG
    _demo();
#endif

    exit(0);
}

void command_line_input(int argc, char *argv[], char **input_file, char **exp_file){
    if (argc == 2){
        *input_file = argv[1];
        *exp_file = NULL;
    }else if(argc == 4){
        if(strcmp(argv[2],"-e") == 0){
            *exp_file = argv[3];
            *input_file = argv[1];
        }else if(strcmp(argv[1], "-e") == 0){
            *exp_file = argv[2];
            *input_file = argv[3];
        }
    }else if(argc == 1 || argc == 3){
        printf("Need more arguments");
        exit(1);
    }
}

void read_file_in_array(char *filename, struct Ntab *ntab){
	FILE *fptr;
	char *line = NULL;
	size_t len = 0;
	ssize_t read;
	
	fptr = fopen(filename, "r");
	while((read = getline(&line, &len, fptr)) != -1){
		add_line(line, ntab);
	}
	
	fclose(fptr);
}

int add_line(char *line, struct Ntab *ntab){
	struct Lines_and_Words *lp;

    if (ntab->lines == NULL){
        ntab->lines = (Lines_and_Words *)malloc(NINIT * sizeof(Lines_and_Words));
        if (ntab->lines == NULL){
            return -1;
        }
        ntab->max_elements = NINIT;
        ntab->index = 0;
    }else if(ntab->index >= ntab->max_elements){
        lp = (Lines_and_Words *) realloc(ntab->lines, (NGROW * ntab->max_elements) * sizeof(Lines_and_Words));
        if (lp == NULL){
            return -1;
        }
        ntab->max_elements *= NGROW;
        ntab->lines = lp;
    }
    strncpy(ntab->lines[ntab->index].array_lines, line, MAX_LINE_LEN);
    return ntab->index++;
}

void store_words(struct Ntab *ntab, node_t **words, int *word_counter){
	int buff_line_num = 0;
	char buffer[MAX_LINE_LEN];
	const char delim[] = " \n";
	char *token;
	char token_temp[MAX_WORD_LEN];
	
	for (int i = 0; i<ntab->index; i++){
		strncpy(buffer, ntab->lines[i].array_lines, MAX_LINE_LEN);
		token = strtok(buffer, delim);
		while (token != NULL){
			
			strncpy(token_temp, token, MAX_WORD_LEN);
			for (int i = 0; i<strlen(token_temp); i++){
				token_temp[i] = tolower(token_temp[i]);
			}
			
			node_t *new_p = new_node(token_temp);
			*words = add_end(*words, new_p);
			*word_counter = *word_counter + 1;
			
			token = strtok(NULL, delim);
		}
		buff_line_num++;
	}
}

void remove_exceptions(node_t **words, node_t **exp_words, int *word_counter){
	node_t *curr;
	node_t *curr2;
	
	for (curr = *words; curr != NULL; curr = curr->next){
		for(curr2 = *exp_words; curr2 != NULL; curr2 = curr2->next){
			if (strcmp(curr->text, curr2->text) == 0){
				printf("%s: %s\n", curr->text, curr2->text);
				*words = remove_word(*words, curr->text);
				*word_counter = *word_counter - 1;
			}
		}
	}
}

node_t *remove_word(node_t *words, char *text){
	node_t *curr, *prev;
	prev = NULL;
	
	for (curr = words; curr != NULL; curr = curr-> next){
		if (strcmp(text, curr->text) == 0) {
			if (prev == NULL){
				words = curr->next;
			}else{
				prev->next = curr->next;
			}
			free(curr);
			return words;
		}
		prev = curr;
	}

	fprintf(stderr, "delitem: %s not in list", text);
	exit(1);
}


void sort(node_t **words, int word_counter){
	char buffer[word_counter][MAX_WORD_LEN];
	node_t *curr = *words;
	int index = 0;
	
	while (curr != NULL && index <= word_counter){
		strncpy(buffer[index], curr->text, MAX_WORD_LEN);
		curr = curr->next;
		index = index + 1;
	}
	
	qsort(buffer, word_counter, MAX_WORD_LEN*sizeof(char), compare);
	*words = NULL;
	
	for (int i=0; i<word_counter; i++){
		node_t *new_p = new_node(buffer[i]);
		*words = add_end(*words, new_p);
	}
}

int compare(const void *a, const void *b) {
    char *sa = (char *)a;
    char *sb = (char *)b;

    return(strcmp(sa, sb));
}

//https://www.geeksforgeeks.org/remove-duplicates-from-a-sorted-linked-list/
void remove_duplicates(node_t **words, int *word_counter){
	node_t *curr = *words;
	node_t *temp;
	
	if (curr == NULL){
		return;
	}
	
	while (curr->next != NULL){
		if (strcmp(curr->text, curr->next->text) == 0){
			temp = curr->next->next;
			free(curr->next);
			curr->next = temp;
		}else{
			curr = curr->next;
		}
	}
}


void print_output(node_t **words, struct Ntab *ntab_lines, int word_counter){
    int occur_count = 0;
	char buffer[MAX_LINE_LEN];
	char word_temp[MAX_WORD_LEN];
	node_t *curr;
	
	int longest = (-1) * (longest_word(words) + 2);
	
	for (curr = *words; curr != NULL; curr = curr->next){
		for (int j = 0; j<ntab_lines->index; j++){
			strncpy(buffer, ntab_lines->lines[j].array_lines, MAX_LINE_LEN);
			
			occur_count = count_words_in_line(curr->text, buffer);
			
			if (occur_count == 1){
				strncpy(word_temp, curr->text, MAX_WORD_LEN);
				for (int m = 0; m<strlen(word_temp); m++){
					word_temp[m] = toupper(word_temp[m]);
				}
				strncpy(&buffer[strlen(buffer)-1], "\0", 1);
				printf("%*s%s (%d)\n", longest, word_temp, buffer, j+1);
			}else if(occur_count > 1){
				strncpy(word_temp, curr->text, MAX_WORD_LEN);
				for (int m = 0; m<strlen(word_temp); m++){
					word_temp[m] = toupper(word_temp[m]);
				}
				strncpy(&buffer[strlen(buffer)-1], "\0", 1);
				printf("%*s%s (%d*)\n", longest, word_temp, buffer, j+1);
			}
		}
	}
}

int longest_word(node_t **words){
    int longest_length = 0;
 	
	node_t *curr;
	for (curr = *words; curr != NULL; curr = curr->next){
		if (strlen(curr->text) > longest_length){
			longest_length = strlen(curr->text);
		}
	}
    return(longest_length);
}

//https://www.tutorialspoint.com/c-program-for-lowercase-to-uppercase-and-vice-versa
int count_words_in_line(char word[MAX_WORD_LEN], char buffer[MAX_LINE_LEN]){
    int word_count = 0;
    int occur_count = 0;
    char temp[MAX_LINE_LEN];
	node_t *words_in_a_line = NULL;
    char *token;
	node_t *curr;

    const char delim[] = " \n";

    strncpy(temp, buffer, MAX_LINE_LEN);
	for (int i = 0; temp[i] != '\0'; i++){
		if (temp[i] >= 'A' && temp[i] <= 'Z'){
			temp[i] = temp[i] + 32;
		}
	}
	
    token = strtok(temp, delim);
    while (token != NULL){
		node_t *new_p = new_node(token);
//		printf("%s\n", new_p->text);
		words_in_a_line = add_end(words_in_a_line, new_p);

        word_count++;

        token = strtok(NULL, delim);
    }

	for (curr = words_in_a_line; curr != NULL; curr = curr->next){
		if (strcmp(curr->text, word) == 0){
			occur_count++;
		}
	}

    return(occur_count);
}
 



	






