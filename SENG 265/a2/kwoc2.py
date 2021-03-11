#!/usr/bin/env python3
import sys
# Main function to define a few variables and make function calls
def main():
    lines, words, exp_lines, exp_words = [],[],[],[]

    filename, exp_file_name = command_line_input()
    if(exp_file_name != None):
        words, lines = get_lines_and_words(filename, words, lines)
        exp_words, exp_lines = get_lines_and_words(exp_file_name, exp_words, exp_lines)
        words = keywords_and_sort(words, exp_words)
        words = remove_duplicates(words)
        print_output(words, lines, filename)
    else:
        words, lines = get_lines_and_words(filename, words, lines)
        words = keywords_and_sort(words, exp_words)
        print_output(words, lines, filename)

# Function to get filename and exception filename from the command line
# Credit: Dr. Zastre, same logic used in kwoc1 used here
def command_line_input():
    if (len(sys.argv) == 2):
        filename = sys.argv[1]
        exp_file_name = None
    elif (len(sys.argv) == 4):
        if (sys.argv[2] == "-e"):
            exp_file_name = sys.argv[3]
            filename = sys.argv[1]
        elif (sys.argv[1] == "-e"):
            exp_file_name = sys.argv[2]
            filename = sys.argv[3]
    elif (len(sys.argv) == 1 or 3):
        print("Need more arguments")
        exit()
        
    return filename, exp_file_name

# Read files and append each line to a list, split lines of input file into words make them lowercase before appending to list 
def get_lines_and_words(filename, words, lines):
    fileptr = open(filename, "r")
    all_lines = fileptr.readlines()
    for item in all_lines:
        lines.append(item.rstrip("\n"))

    for line in lines:
        [words.append(x) for x in line.lower().split()]
    fileptr.close()

    return words, lines

# Function to extract keywords from list of words made by previous function
# Credit Idea adopted from https://www.geeksforgeeks.org/python-remove-duplicates-list/ 
def keywords_and_sort(words, exp_words):
    after_exp_words = []
    [after_exp_words.append(x) for x in words if x not in exp_words]
    after_exp_words.sort()
    return after_exp_words

# Function to remove any duplicate words from the list of words
# Same idea in the above function was used here 
def remove_duplicates(words):
    final_words = []
    [final_words.append(x) for x in words if x not in final_words]
    return final_words

# Function will provide the desired output which is as follows:
# Keyword in caps, indent by longest word + 2 spaces, what line the word occured in and number of times it occured
def print_output(words, lines, filename):
    occur_count = 0
    longest = 0
    buffer_line = []

    longest = (-1) * (longest_word(words, longest) + 2)
    
    for i in range(len(words)):
        for j in range(len(lines)):
            buffer_line = lines[j]
            occur_count = count_words_in_line(words[i], buffer_line, occur_count)

            if (occur_count == 1):
                word_temp = [x.upper() for x in words]
                print("%*s%s (%d)"% (longest, word_temp[i], buffer_line, j+1))
            elif (occur_count > 1):
                word_temp = [x.upper() for x in words]
                print("%*s%s (%d*)"% (longest, word_temp[i], buffer_line, j+1))

# Function to find the length of the longest keyword
def longest_word(words, longest):
    for i in range (len(words)):
        if (len(words[i]) > longest):
            longest = len(words[i])

    return longest

# Function to count the occurances of a word in a single line
def count_words_in_line(word, buffer_line, occur_count):
    temp_line = buffer_line.lower().split()
    occur_count = temp_line.count(word)

    return occur_count
    
if __name__ == "__main__":
    main()