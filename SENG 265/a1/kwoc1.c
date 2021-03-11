#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<ctype.h>

#define MAX_LINE_NUM 100
#define MAX_LINE_LEN 80
#define MAX_WORDS 500
#define MAX_WORD_LEN 20
#define MAX_WORDS_PER_LINE 40


//Two global arrays to store the file words and exception file words repectively
char file_words[MAX_WORDS][MAX_WORD_LEN];
char exp_file_words[MAX_WORDS][MAX_WORD_LEN];

//Two global integers to store the number of file words and number of exception file words repectively
int file_word_counter = 0;
int exp_word_counter = 0;


//function to open the file, read line by line and store it in an array
//Credit: Dr. Zastre for this code (shown in class)
void read_file(int *line_counter, char *filename, char arr[MAX_LINE_NUM][MAX_LINE_LEN]){
    FILE *fptr;
    char read_line[MAX_LINE_LEN];
    fptr = fopen(filename, "r");
    while(fgets(read_line, MAX_LINE_LEN, fptr) != NULL){
        strncpy(arr[*line_counter], read_line, MAX_LINE_LEN);
        *line_counter = *line_counter + 1;
    }
    fclose(fptr);
}

//function to tokenize the array of lines and store them into another array word by word
//Credit: Dr. Zastre for this code (shown in class)
void store_words(char lines[MAX_LINE_NUM][MAX_LINE_LEN], int *line_counter, char words[MAX_WORDS][MAX_WORD_LEN], int *word_counter){
    int buff_line_num = 0;
    char buffer[MAX_LINE_NUM];
    const char delim[] = " \n";
    char *token;
    
    for (int i = 0; i<*line_counter; i++){
        strncpy(buffer, lines[buff_line_num], MAX_LINE_LEN);
        token = strtok(buffer, delim);
        while(token != NULL){
            strncpy(words[*word_counter], token, MAX_WORD_LEN);
            *word_counter = *word_counter + 1;

            token = strtok(NULL, delim);
        }
        buff_line_num++;
    }
}

//Function to extract keywords from the list of words made by the previous function
//Idea adopted from https://www.sanfoundry.com/c-program-delete-repeated-words-string/
void remove_exceptions(char file_words[MAX_WORDS][MAX_WORD_LEN], char exp_file_words[MAX_WORDS][MAX_WORD_LEN], int *file_word_counter, int exp_word_counter){
    char buffer[MAX_WORDS][MAX_WORD_LEN];
    int words = 0;
    for (int i = 0; i<*file_word_counter; i++){
        strncpy(buffer[i], file_words[i], MAX_WORD_LEN);
    }
    
    for (int i = 0; i<*file_word_counter; i++){
        for (int j = 0; j<exp_word_counter; j++){
            if (strcmp(file_words[i], exp_file_words[j]) == 0){
                strncpy(buffer[i], "^", MAX_WORD_LEN);
            }
        }
    }
    
    for (int m = 0; m<*file_word_counter; m++){
        if (strcmp(buffer[m], "^") != 0){
            strncpy(file_words[words], buffer[m], MAX_WORD_LEN);
            words = words + 1;
        }
    }
    strncpy(file_words[words+1], "\0", MAX_WORD_LEN);
    *file_word_counter = words;
}

//Function to remove ang duplicate keywords from the list of words
//Idea adopted from https://www.sanfoundry.com/c-program-delete-repeated-words-string/
void remove_duplicates(char file_words[MAX_WORDS][MAX_WORD_LEN], int *file_word_counter){
    int words = 0;
    char buffer[MAX_WORDS][MAX_WORD_LEN];
    for (int i = 0; i<*file_word_counter; i++){
        strncpy(buffer[i], file_words[i], MAX_WORD_LEN);
    }
    
    for (int i = 0; i<*file_word_counter; i++){
        for (int j = i+1; j<*file_word_counter; j++){
            if (strcmp(file_words[i], file_words[j]) == 0){
                strncpy(buffer[j], "^", MAX_WORD_LEN);
            }
        }
    }
    
    for (int m = 0; m<*file_word_counter; m++){
        if (strcmp(buffer[m], "^") != 0){
            strncpy(file_words[words], buffer[m], MAX_WORD_LEN);
            words = words + 1;
        }
    }
    strncpy(file_words[words], "\0", MAX_WORD_LEN);
    *file_word_counter = words;
}

//Function used in the qsort call to sort the words alphabetically
//Credit: Dr. Zastre for this code (shown in class)
int compare(const void *a, const void *b) {
    char *sa = (char *)a;
    char *sb = (char *)b;

    return(strcmp(sa, sb));
}

//Function to count the occurances of a word in a single line
int count_words_in_line(char words[MAX_WORDS], char buffer[MAX_LINE_LEN]){
    int word_count = 0;
    int occur_count = 0;
    char temp[MAX_LINE_LEN];
    char words_in_a_line[MAX_WORDS_PER_LINE][MAX_WORD_LEN];
    char *token;
    const char delim[] = " \n";
    
    strncpy(temp, buffer, MAX_LINE_LEN);
    token = strtok(temp, delim);
    while (token != NULL){
        strncpy(words_in_a_line[word_count], token, MAX_WORD_LEN);
        word_count++;
        token = strtok(NULL, delim);
    }
    
    for (int i = 0; i<word_count; i++){
        if (strcmp(words, words_in_a_line[i]) == 0){
            occur_count++;
        }
    }
    return(occur_count);
}

//Funtion to find the longest word in the input file
int longest_word(char file_words[MAX_WORDS][MAX_WORD_LEN], int file_word_counter){
    int longest_length = 0;
    for (int i = 0; i<file_word_counter; i++){
        if (strlen(file_words[i]) > longest_length){
            longest_length = strlen(file_words[i]);
        }
    } 
    return(longest_length);
}

//Function that will provide the desired output which is as follows:
//Keyword in caps, indent by longest word + 2 spaces, what line the word occured in and number of times it occured
void print_output(char file_words[MAX_WORDS][MAX_WORD_LEN], char lines[MAX_LINE_NUM][MAX_LINE_LEN], int word_counter, int *line_counter){
    int occur_count = 0;
    char buffer[MAX_LINE_LEN];
    char word_temp[MAX_WORD_LEN];
    
    int longest = (-1) * (longest_word(file_words, word_counter) + 2);

    for (int i = 0; i<word_counter; i++){
        for (int j = 0; j<*line_counter; j++){
            strncpy(buffer, lines[j], MAX_LINE_LEN);
            
            occur_count = count_words_in_line(file_words[i], buffer);
            
            if (occur_count == 1){
                strncpy(word_temp, file_words[i], MAX_WORD_LEN);
                for (int m = 0; m<strlen(word_temp); m++){
                    word_temp[m] = toupper(word_temp[m]);
                }
                strncpy(&buffer[strlen(buffer)-1], "\0", 1);
                printf("%*s%s (%d)\n", longest, word_temp, buffer, j+1);
            }else if(occur_count > 1){
                strncpy(word_temp, file_words[i], MAX_WORD_LEN);
                for (int m = 0; m<strlen(word_temp); m++){
                    word_temp[m] = toupper(word_temp[m]);
                }
                strncpy(&buffer[strlen(buffer)-1], "\0", 1);
                printf("%*s%s (%d*)\n", longest, word_temp, buffer, j+1);
            }
          
        }
    }
}

//Main function to initialize variables and to call functions
int main(int argc, char *argv[]){
    
    int line_counter = 0;
    char *filename = NULL;
    char lines[MAX_LINE_NUM][MAX_LINE_LEN];
    
    int exp_line_counter = 0;
    char *exp_filename = NULL;
    char exp_lines[MAX_LINE_NUM][MAX_LINE_LEN];
    
    if (argc == 2){
        filename = argv[1];
        read_file(&line_counter, filename, lines);
        store_words(lines, &line_counter, file_words, &file_word_counter);
        qsort(file_words, file_word_counter, MAX_WORD_LEN*sizeof(char), compare);
        remove_duplicates(file_words, &file_word_counter);
        print_output(file_words, lines, file_word_counter, &line_counter);
    }else if(argc == 4){
        if(strcmp(argv[1], "-e") == 0){
            filename = argv[3];
            exp_filename = argv[2];
            
            read_file(&line_counter, filename, lines);
            store_words(lines, &line_counter, file_words, &file_word_counter);

            read_file(&exp_line_counter, exp_filename, exp_lines);
            store_words(exp_lines, &exp_line_counter, exp_file_words, &exp_word_counter);

            remove_exceptions(file_words, exp_file_words, &file_word_counter, exp_word_counter);
            qsort(file_words, file_word_counter, MAX_WORD_LEN*sizeof(char), compare);
            remove_duplicates(file_words, &file_word_counter);
            print_output(file_words, lines, file_word_counter, &line_counter);
        }else if(strcmp(argv[2], "-e") == 0){
            filename = argv[1];
            exp_filename = argv[3];
            
            read_file(&line_counter, filename, lines);
            store_words(lines, &line_counter, file_words, &file_word_counter);

            read_file(&exp_line_counter, exp_filename, exp_lines);
            store_words(exp_lines, &exp_line_counter, exp_file_words, &exp_word_counter);

            remove_exceptions(file_words, exp_file_words, &file_word_counter, exp_word_counter);
            qsort(file_words, file_word_counter, MAX_WORD_LEN*sizeof(char), compare);
            remove_duplicates(file_words, &file_word_counter);
            print_output(file_words, lines, file_word_counter, &line_counter);
            
        }
    }
    return(0);
}

