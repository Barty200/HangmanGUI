import pygame
from random import randint
import os
#os.chdir("Hangman/")

pygame.font.init()
mainFont = pygame.font.SysFont('Comic Sans MS', 25)
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
gameLoop = True

letterObjects = []
lettersXStart = 50
lettersXIncrease = 50
lettersMaxInRow = 14
lettersYStart = 50
lettersYIncrease = 50

with open('words.txt') as word_file:
    wordsToChooseFrom = word_file.read().split()

correctWord = []
currentWord = []
wordXStart = 50
wordXIncrease = 50

numberWrongGuesses = 0

hangmanImages = []

for i in range(1, 12):
    hangmanImages.append(pygame.image.load(f"Images\\{i}.png"))

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")


class Button:
    def __init__(self, letter, x, y, diameter):
        self.letter = letter
        self.pressed = False
        self.x = x
        self.y = y
        self.diameter = diameter

    def Pressed(self, position):
        if not self.pressed:
            differenceX = self.x - position[0]
            differenceY = self.y - position[1]
            if differenceX < self.diameter and differenceX > -self.diameter and differenceY < self.diameter and differenceY > -self.diameter:
                self.pressed = True
                self.foundLetter = False
                for i in range(len(correctWord)):
                    if correctWord[i] == self.letter:
                        currentWord[i] = correctWord[i]
                        self.foundLetter = True
                if not self.foundLetter:
                    global numberWrongGuesses
                    numberWrongGuesses += 1

    def Draw(self, window):
        if not self.pressed:
            pygame.draw.circle(window, (0,0,0), (self.x, self.y), self.diameter)
            textsurface = mainFont.render(self.letter, False, (255,255,255))
            window.blit(textsurface, ((self.x - (self.diameter/2)), (self.y - (self.diameter/2) - 8)))


def display_currentWord(window):
    wordXStart = (SCREEN_WIDTH / 2) - ((len(correctWord) * 50) / 2)
    for i in currentWord:
        textsurface = mainFont.render(str(i), False, (0,0,0))
        window.blit(textsurface, (wordXStart, 300))
        wordXStart += wordXIncrease


def redrawWindow(window):
    global numberWrongGuesses
    global correctWord
    global currentWord
    window.fill((255,255,255))

    for i in letterObjects:
        i.Draw(window)

    if not numberWrongGuesses == 0 and not (numberWrongGuesses >= 12):
        window.blit(hangmanImages[numberWrongGuesses - 1], (0, 400))
    elif numberWrongGuesses >= 12:
        localCorrectWord = ""
        for i in correctWord:
            localCorrectWord += i
        currentWord = []
        correctWord = []
        numberWrongGuesses = 0
        redrawWindow(window)
        textsurface = mainFont.render("You ran out of guesses!", False, (0,0,0))
        window.blit(textsurface, (200, 300))
        pygame.display.update()
        pygame.time.delay(1000)
        redrawWindow(window)
        textsurface = mainFont.render(f"The word was: {localCorrectWord}", False, (0,0,0))
        window.blit(textsurface, (200, 300))
        pygame.display.update()
        pygame.time.delay(1000)
        for i in letterObjects:
            i.pressed = False
        pickRandomWord()

    display_currentWord(window)

    pygame.display.update()

def pickRandomWord():
    randomIndex = randint(0, len(wordsToChooseFrom) - 1)
    word = wordsToChooseFrom[randomIndex]
    for i in word:
        correctWord.append(i.upper())
        if not i == " ":
            currentWord.append("_")
        else:
            currentWord.append(" ")

for i in range(65, 91):
    letter = chr(i)
    button = Button(letter, lettersXStart, lettersYStart, 20)
    letterObjects.append(button)
    lettersXStart += lettersXIncrease
    if lettersXStart == lettersMaxInRow * lettersXIncrease:
        lettersXStart = 50
        lettersYStart += lettersYIncrease

pickRandomWord()

while gameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in letterObjects:
                i.Pressed(pygame.mouse.get_pos())

    if currentWord == correctWord:
        localCorrectWord = ""
        for i in correctWord:
            localCorrectWord += i
        currentWord = []
        correctWord = []
        numberWrongGuesses = 0
        redrawWindow(window)
        textsurface = mainFont.render("You guessed the word!", False, (0,0,0))
        window.blit(textsurface, (200, 300))
        pygame.display.update()
        pygame.time.delay(1000)
        redrawWindow(window)
        textsurface = mainFont.render(f"The word was: {localCorrectWord}", False, (0,0,0))
        window.blit(textsurface, (200, 300))
        pygame.display.update()
        pygame.time.delay(1000)
        for i in letterObjects:
            i.pressed = False
        pickRandomWord()

    redrawWindow(window)