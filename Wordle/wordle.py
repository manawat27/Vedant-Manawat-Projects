from turtle import width
import pygame,random,sys
from pygame.locals import *
pygame.init()

class cosmetics:
    white = (255,255,255)
    yellow = (255,255,102)
    green = (0,255,0)
    gray = (211,211,211)
    black = (0,0,0)

    font = pygame.font.SysFont("Helvetica neue", 40)
    bigFont = pygame.font.SysFont("Helvetica neue", 80)
    win =  bigFont.render("You Win!", True, green)
    lose =  bigFont.render("You Lose!", True, green)
    playAgain = bigFont.render("Play Again?", True, green)

def checkGuess(turnNumber, word, guess, window):
    lettersToDraw = ["","","","",""]
    space = 0 ## space between each letter
    guessColors = [cosmetics.gray,cosmetics.gray,cosmetics.gray,cosmetics.gray,cosmetics.gray]

    for x in range(0,5):
        if guess[x] in word:
            guessColors[x] = cosmetics.yellow

        if word[x] == guess[x]:
            guessColors[x] = cosmetics.green

    list(guess)

    for i in range(0,5):
        lettersToDraw[i] = cosmetics.font.render(guess[i], True, cosmetics.black)
        pygame.draw.rect(window, guessColors[i], pygame.Rect(60 + space, 50 + (turnNumber*80), 50, 50))
        window.blit(lettersToDraw[i], (70 + space, 60 + (turnNumber*80)))
        space += 80

    if guessColors == [cosmetics.green,cosmetics.green,cosmetics.green,cosmetics.green,cosmetics.green]:
        return True

def main():
    file = open("wordList.txt",'r')
    wordList = file.readlines()
    word = wordList[random.randint(0,len(wordList)-1)].upper()

    height = 600
    width = 500

    FPS = 60
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((width,height))
    window.fill(cosmetics.black)

    guess = ""
    print(word)

    for x in range(0,5):
        for y in range(0,5):
            pygame.draw.rect(window,cosmetics.gray,pygame.Rect(60+(x*80), 50+(y*80), 50, 50),2)
    
    pygame.display.set_caption("Wordle!")

    attempts = 0
    win_check = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.exit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                guess += event.unicode.upper()

                if event.key == K_RETURN and win_check == True:
                    main()

                if event.key == K_RETURN and attempts == 6:
                    main()
            
                if event.key == pygame.K_BACKSPACE or len(guess) > 5:
                    guess = guess[:-1]
                
                if event.key == K_RETURN and len(guess) > 4:
                    win_check = checkGuess(attempts, word, guess, window)
                    attempts += 1
                    guess = ""
                    window.fill(cosmetics.black,(0,500,500,200))
        
        window.fill(cosmetics.black,(0,500,500,200))
        renderGuess = cosmetics.font.render(guess,True,cosmetics.gray)
        window.blit(renderGuess, (180,530))

        if win_check == True:
            window.blit(cosmetics.win, (90,200))
            window.blit(cosmetics.playAgain,(60,300))
        
        if attempts == 6 and win_check != True:
            window.blit(cosmetics.lose, (90,200))
            window.blit(cosmetics.playAgain,(60,300))
        
        pygame.display.update()
        clock.tick(FPS)
main()