/*
 Name: Vedant Manawat
 VNumber: V00904582
 
 Feb. 12 2021
 CSC 360 Assignment 1
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>

#define MAX_ARGUMENTS 7
#define MAX_INPUT_LEN 80
#define MAX_PATH_LEN 80
#define MAX_PROMPT_LEN 10
#define MAX_DIRECTORIES 10
#define MAX_ARGUMENT_LEN 12

//Source of code: This code was implemented by my in the Spring semester of 2020 for assignment 1 (kwoc1.c) of the course SENG 265
void  parse_binary_file(char file_input[MAX_DIRECTORIES][MAX_PATH_LEN], int *line_counter){
    FILE *fptr;
    char read_line[MAX_PATH_LEN];
    fptr = fopen(".sh360rc", "rb");
    while(fgets(read_line, MAX_PATH_LEN, fptr) != NULL){
        strncpy(file_input[*line_counter], read_line, MAX_PATH_LEN);
        *line_counter = *line_counter + 1;
    }
    fclose(fptr);
}

//Source of code: This code was implemented by my in the Spring semester of 2020 for assignment 1 (kwoc1.c) of the course SENG 265
void tokenize_input_file(char file_input[MAX_DIRECTORIES][MAX_PATH_LEN],char parsed_file_input[MAX_DIRECTORIES][MAX_PATH_LEN], int *line_counter){
    char *t;
    int num_toks = 0;
    int buff_counter = 0;
    const char delim[] = "\n";
    char buffer[MAX_PATH_LEN];
    
    for (int i=0; i<*line_counter; i++){
        strncpy(buffer, file_input[buff_counter], MAX_PATH_LEN);
        t = strtok(buffer, delim);
        while(t != NULL){
            strncpy(parsed_file_input[num_toks], t, MAX_PATH_LEN);
            num_toks = num_toks + 1;
            t = strtok(NULL, delim);
        }
        buff_counter = buff_counter + 1;
    }
}

//The credit for this code goes to Dr. Zastre, this code was inspired by the code provided in appendix_e.c
void tokenize_user_input(char user_input[MAX_INPUT_LEN], char *parsed_user_input[MAX_INPUT_LEN],int *num_tokens){
    char *t;
    
    *num_tokens = 0;
    
    t = strtok(user_input, " ");
    while (t != NULL && *num_tokens < MAX_ARGUMENTS) {
        parsed_user_input[*num_tokens] = t;
        *num_tokens = *num_tokens + 1;
        t = strtok(NULL, " ");
    }
}

//The purpose of this code is to parse through the users input and identify which tokens are an option to the command the proceed
void formulate_args(char *parsed_user_input[MAX_ARGUMENTS],char *arguments[MAX_ARGUMENT_LEN],int *argument_counter, int *num_tokens){
    
    if (strcmp(parsed_user_input[0],"OR") == 0){
        for (int i=2; i<*num_tokens; i++){
            if (strcmp(parsed_user_input[i],"->") == 0){
                return;
            }else{
                arguments[i-2] = parsed_user_input[i];
            }
            *argument_counter = *argument_counter + 1;
        }
        
    }else{
        for (int i=1; i<*num_tokens; i++){
            arguments[i-1] = parsed_user_input[i];
            *argument_counter = *argument_counter + 1;
        }
    }
}

void formulate_pipe_args(char *parsed_user_input[MAX_ARGUMENTS],char *arguments_head[MAX_ARGUMENT_LEN],char *arguments_body[MAX_ARGUMENT_LEN],char *arguments_tail[MAX_ARGUMENT_LEN],int *argument_head_counter, int *num_tokens){

    for (int i=2; i<*num_tokens; i++){
        if (strcmp(parsed_user_input[i],"->") == 0){
            return;
        }else{
            arguments_head[i-2] = parsed_user_input[i];
            *argument_head_counter = *argument_head_counter + 1;
        }
    }
    
    for (int i=0; i<*argument_head_counter; i++){
        printf("%s",arguments_head[i]);
    }
}

/*The purpose of this function is to formulate the path to for each command if it command has a pipe in it
    
    The way this function would work is, it would parse the tokens of the users input and separate the command head, command body and command tail
    For example if the command was: PP ls -la -> grep 'root' -> wc
        Then the command head would be ls, command body would be grep and command tail would be wc
 
 Unfortunately this function is not complete as the implementer did not have enough time to finish it
*/
void get_commands(char *parsed_user_input[MAX_ARGUMENTS], int *num_tokens,char temp_head_cmd[MAX_INPUT_LEN], char temp_body_cmd[MAX_INPUT_LEN], char temp_tail_cmd[MAX_INPUT_LEN]){

    
    for (int i=2; i<*num_tokens; i++){
        if (strcmp(parsed_user_input[i], "->") == 0){
            strncpy(temp_tail_cmd, parsed_user_input[i+1],MAX_INPUT_LEN);
        }
    }
    
    strncpy(temp_head_cmd, parsed_user_input[1],MAX_INPUT_LEN);
    
}

/*The purpose of this function is to formulate the path to for each command for an input that uses pipe
    
    The general idea behind this function is the same as the one mentioned above (formulate_commands) the only difference is that it doesnt make a call to another function to check if the path exists and is executable
 
 Unfortunately this function is not complete (does not formulate the path for the command body) as the implementer did not have enough time to finish it
*/
void formulate_pipe_commands(char parsed_file_input[MAX_PATH_LEN], char command_head[MAX_INPUT_LEN], char command_body[MAX_INPUT_LEN], char command_tail[MAX_INPUT_LEN],char head[MAX_INPUT_LEN],char body[MAX_INPUT_LEN],char tail[MAX_INPUT_LEN]){
    
    char buffer_head_path[MAX_PATH_LEN];
    char buffer_tail_path[MAX_PATH_LEN];
    
    strncpy(buffer_head_path, parsed_file_input,MAX_PATH_LEN);
    strncat(buffer_head_path, "/",1);
    strncat(buffer_head_path,head,strlen(head));
    strncpy(command_head,buffer_head_path,MAX_PATH_LEN);
    
    strncpy(buffer_tail_path, parsed_file_input,MAX_PATH_LEN);
    strncat(buffer_tail_path, "/",1);
    strncat(buffer_tail_path,tail,strlen(tail));
    strncpy(command_tail,buffer_tail_path,MAX_PATH_LEN);
}

/*
 The purpose of this function is to extract the filename from the user input if the command that was entered used an OR for redirection of the output
 */
void get_file_name(char filename[30],char *parsed_user_input[MAX_ARGUMENTS],int *num_tokens){
    
    int index_copy;
    for (int i=0;i<*num_tokens; i++){
        if (strcmp(parsed_user_input[i],"->") == 0){
            index_copy = i;
        }
    }
    strncpy(filename, parsed_user_input[index_copy+1],strlen(parsed_user_input[index_copy+1]));
}

/* The credit for this code goes to:
    - https://www.unix.com/programming/24159-how-check-if-directory-file-exist-using-c-c.html
    - https://stackoverflow.com/questions/4629643/implementing-a-unix-shell-in-c-check-if-file-is-executable
 
 This functions justs checks whether the path it has been given (for eg: /bin/ls) exists and if its executable, if so return 1, else return 0
*/
int check_if_exists_and_executable(char command[MAX_PATH_LEN]){
    struct stat st;
    if (stat(command,&st) == 0){
        if (access(command, F_OK|X_OK)==0){
            return 1;
        }else{
            return 0;
            fprintf(stdout, "%s: echo: Not executable\n",command);
        }
    }else{
        return 0;
        fprintf(stdout, "%s: echo: No such file or directory\n",command);
    }
}

int formulate_commands(char parsed_file_input[MAX_PATH_LEN],char user_input[MAX_INPUT_LEN],char *parsed_user_input[MAX_ARGUMENTS], char command[MAX_PATH_LEN],int *line_counter,int *execute){

    char buffer_path[MAX_PATH_LEN];
    char buffer_user_input[MAX_INPUT_LEN];
    char *t;

    if (strstr(user_input,"OR")){
        strncpy(buffer_path, parsed_file_input,MAX_PATH_LEN);
        strncpy(buffer_user_input,parsed_user_input[1],MAX_INPUT_LEN);
        strncat(strncat(buffer_path,"/",1),buffer_user_input,MAX_PATH_LEN);
        strncpy(command, buffer_path, MAX_PATH_LEN);
        
        *execute = check_if_exists_and_executable(command);
        return *execute;
    }else{
        strncpy(buffer_path, parsed_file_input,MAX_PATH_LEN);
        strncpy(buffer_user_input,user_input,MAX_INPUT_LEN);
        t = strtok(buffer_user_input, " ");
        strncat(strncat(buffer_path,"/",1),t,MAX_PATH_LEN);
        strncpy(command, buffer_path, MAX_PATH_LEN);

        *execute = check_if_exists_and_executable(command);
        return *execute;
    }
    
}

/*
 The credit for this code goes to Dr. Zastre, this code was taken from appendix_d.c
 This functions purpose is to set up the arguments and other variables needed to able to pipe two commands and then provide them to execve to run the commands as a pipe
 */
void execute_pipe(char command_head[MAX_INPUT_LEN],char command_tail[MAX_INPUT_LEN]){

    char *cmd_head[] = { command_head, 0, 0 };
    char *cmd_tail[] = { command_tail,0, 0 };
    char *envp[] = { 0 };
    int status;
    int pid_head, pid_tail;
    int fd[2];

    pipe(fd);

    if ((pid_head = fork()) == 0) {
        dup2(fd[1], 1);
        close(fd[0]);
        execve(cmd_head[0], cmd_head, envp);
    }

    if ((pid_tail = fork()) == 0) {
        dup2(fd[0], 0);
        close(fd[1]);
        execve(cmd_tail[0], cmd_tail, envp);
    }

    close(fd[0]);
    close(fd[1]);

    waitpid(pid_head, &status, 0);
    waitpid(pid_tail, &status, 0);
}



int main(int argc, char *argv[]){
    
    /* ####################### DECLARING VARIABLES ####################### */
    char file_input[MAX_DIRECTORIES][MAX_PATH_LEN];
    char parsed_file_input[MAX_DIRECTORIES][MAX_PATH_LEN];
    char user_input[MAX_INPUT_LEN];
    char *parsed_user_input[MAX_INPUT_LEN];
    char command[MAX_INPUT_LEN];
    char *arguments[MAX_ARGUMENT_LEN],*arguments_head[MAX_ARGUMENT_LEN],*arguments_body[MAX_ARGUMENT_LEN],*arguments_tail[MAX_ARGUMENT_LEN];
    char *envp[] = { 0 };
    char filename[30];

    char head[MAX_INPUT_LEN], command_head[MAX_INPUT_LEN];
    char body[MAX_INPUT_LEN], command_body[MAX_INPUT_LEN];
    char tail[MAX_INPUT_LEN], command_tail[MAX_INPUT_LEN];
    int num_tokens,pid,status,execute,fd,execute_head,execute_body,execute_tail;
    int line_counter = 0;
    int argument_counter = 0;
    int argument_head_counter = 0;

    
    //Function calls to parse the .sh360rc file and tokenize it
    parse_binary_file(file_input, &line_counter);
    tokenize_input_file(file_input,parsed_file_input, &line_counter);
    
    /* The credit for the general structure of this for loop and how to make calls to execve goes to Dr. Zastre
        This code was inspired from all of the appendix files provided to us
     */
    for (;;){
        fprintf(stdout, "%s ", parsed_file_input[0]);
        fflush(stdout);
        
        fgets(user_input, MAX_INPUT_LEN, stdin);

        if (user_input[strlen(user_input) - 1] == '\n') {
            user_input[strlen(user_input) - 1] = '\0';
        }
        
        
        //Function calls to tokenize and formulate the arguments based on the user input
        tokenize_user_input(user_input, parsed_user_input, &num_tokens);
        formulate_args(parsed_user_input,arguments,&argument_counter,&num_tokens);
        
        if ((strcmp(user_input, "exit") == 0)) {
            exit(1);
        }
        
        if (num_tokens > MAX_ARGUMENTS){
            fprintf(stdout, "Number of arguments (%d) exceed limit of 7",num_tokens);
            exit(1);
        }
        
        /* This is where the set up is done if the user wishes to pipe commands
            From here appropriate function calls are made to then actually run the execve for the pipe
         */
        if (strstr(user_input,"Pipe")){
            formulate_pipe_args(parsed_user_input,arguments_head,arguments_body,arguments_tail,&argument_head_counter,&num_tokens);
            if (num_tokens == 4){
                for (int i=1; i<line_counter; i++){
                    get_commands(parsed_user_input, &num_tokens,head, body, tail);
                    char temp_head_cmd[MAX_INPUT_LEN];
                    char temp_tail_cmd[MAX_INPUT_LEN];
                    char temp_body_cmd[MAX_INPUT_LEN];
                    formulate_pipe_commands(parsed_file_input[i],temp_head_cmd,temp_body_cmd,temp_tail_cmd,head,body,tail);

                    if (check_if_exists_and_executable(temp_head_cmd) == 1){
                        execute_head = 1;
                        strncpy(command_head,temp_head_cmd,MAX_INPUT_LEN);
                    }

                    if (check_if_exists_and_executable(temp_tail_cmd) == 1){
                        execute_tail = 1;
                        strncpy(command_tail,temp_tail_cmd,MAX_INPUT_LEN);
                    }
                }
                execute_pipe(command_head,command_tail);
            }else if (num_tokens>4){
                for (int i=1; i<line_counter; i++){
                    get_commands(parsed_user_input,&num_tokens,head,body,tail);
                    char temp_head_cmd[MAX_INPUT_LEN];
                    char temp_tail_cmd[MAX_INPUT_LEN];
                    char temp_body_cmd[MAX_INPUT_LEN];
                    formulate_pipe_commands(parsed_file_input[i],temp_head_cmd,temp_body_cmd,temp_tail_cmd,head,body,tail);

                    // printf("%s",temp_head_cmd);
                    // printf("\n");
                    // printf("%s",temp_body_cmd);
                    // printf("\n");
                    // printf("%s",temp_tail_cmd);
                    // printf("\n");

                    if (check_if_exists_and_executable(temp_head_cmd) == 1){
                        execute_head = 1;
                        strncpy(command_head,temp_head_cmd,MAX_INPUT_LEN);
                    }

                    if (check_if_exists_and_executable(temp_tail_cmd) == 1){
                        execute_tail = 1;
                        strncpy(command_tail,temp_tail_cmd,MAX_INPUT_LEN);
                    }
                }
                execute_pipe(command_head,command_tail);
            }
        }

        /* This is where the set up is done if the user wishes to redirect the output of commands to a file
            From here appropriate function calls are made to then actually run the execve for the redirection
         */
        if (strstr(user_input,"OR")){
            get_file_name(filename,parsed_user_input,&num_tokens);
            if ((pid=fork())==0){
                if (num_tokens == 4){
                    fd = open(filename, O_CREAT|O_RDWR, S_IRUSR|S_IWUSR);
                    for (int i=1; i<line_counter; i++){
                        formulate_commands(parsed_file_input[i],user_input,parsed_user_input,command,&line_counter,&execute);
                        if (fd == -1){
                            fprintf(stderr, "cannot open %s for writing\n",filename);
                            exit(1);
                        }
                        dup2(fd, 1);
                        dup2(fd, 2);
                        char *args[] = {command, 0,0};
                        if (execute == 1){
                            execve(args[0],args,envp);
                        }
                    }
                }else if(num_tokens>4){
                    fd = open(filename,O_CREAT|O_RDWR, S_IRUSR|S_IWUSR);
                    for (int i=1; i<line_counter; i++){
                        formulate_commands(parsed_file_input[i],user_input,parsed_user_input,command,&line_counter,&execute);

                        int size_of_args = num_tokens + 1;
                        char *args[size_of_args];

                        args[0] = command;
                        for(int i=1; i<num_tokens; i++){
                            args[i] = arguments[i-1];
                        }

                        args[size_of_args-1] = 0;

                       if (fd == -1){
                           fprintf(stderr, "cannot open %s for writing\n",filename);
                           exit(1);
                        }

                        dup2(fd, 1);
                        dup2(fd, 2);

                        if (execute == 1){
                            execve(args[0],args,envp);
                        }
                    }
                }
            }
            waitpid(pid, &status, 0);
        }
        
        /* This is where the set up is done if the user wishes to general commands
            From here appropriate function calls are made to then actually run the execve for the commands
         */
        if((pid = fork())==0){
            if (num_tokens == 1){
                for (int i=1; i<line_counter; i++){
                    formulate_commands(parsed_file_input[i],user_input,parsed_user_input,command,&line_counter,&execute);
                    char *args[] = {command, 0,0};
                    if (execute == 1){
                        execve(args[0],args,envp);
                    }
                }
            }else if (num_tokens > 1){
                for (int i=1; i<line_counter; i++){
                    formulate_commands(parsed_file_input[i],user_input,parsed_user_input,command,&line_counter,&execute);

                    int size_of_args = num_tokens + 1;
                    char *args[size_of_args];

                    args[0] = command;
                    for(int i=1; i<num_tokens; i++){
                        args[i] = arguments[i-1];
                    }

                    args[size_of_args-1] = 0;
                    if (execute==1){
                        execve(args[0],args,envp);
                    }
                }
            }
        }

        while (wait(&status) > 0) {
        }
    }
}