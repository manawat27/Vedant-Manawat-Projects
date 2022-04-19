import random 
import resources
wordlist = "airplane vehicle television speaker computer giraffe fox bunny bumblebee farmer grass orchard apple fallout house".upper().split()
random.shuffle(wordlist)

secret_word = wordlist.pop()
correct_letters = []
incorrect_letters = []

def draw_board():
    # Draw gallows and display the word
    print(resources.hangman_board[len(incorrect_letters)])
    for i in secret_word:
        if i in correct_letters:
            print(i, end=' ')
        else:
            print('_', end=' ')
    print("\n\n")
    print("*** MISSED LETTERS ***")
    for i in incorrect_letters:
        print(i, end=' ')
    print("\n**********************")

def guess():
    # Allow user to make a guess and append to correct or incorrect
    while True:
        guess_letter = input("guess a letter\n: ").upper()
        if guess_letter in correct_letters or guess_letter in incorrect_letters:
            print("You have alredy guessed this letter. Guess again.")
        elif guess_letter.isnumeric():
            print("Please only enter letters. Guess again")
        elif len(guess_letter) > 1:
            print("Pleas only enter one letter at a time. Guess again")
        elif len(guess_letter) == 0:
            print("Please enter a letter")
        else:
            break
    
    if guess_letter in secret_word:
        correct_letters.append(guess_letter)
    else:
        incorrect_letters.append(guess_letter)

def win_lose():
    # Check to see if user has won or lost game
    if len(incorrect_letters) > 5:
        return "LOST"
    for i in secret_word:
        if i not in correct_letters:
            return "NO WIN"
    return "WIN"

while True:
    draw_board()
    guess()
    win_condition = win_lose()
    if win_condition == "LOST":
        print("GAME OVER! HE WORD WAS *** ", secret_word, " ***")
        print(resources.hangman_board[6])
        break
    elif win_condition == "WIN":
        print("YOU WIN! THE WORD WAS *** ", secret_word, " ***")
        break
