import requests
import random

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
listOfWords = response.content.splitlines()[1:]

gameStartText = "Welcome to Hangman. Enter 'b' to begin. Enter '#q' at any point to exit. :-)"

# The hangman is not displayed (sorry).
def gameRun():
    print("Let's begin!")
    answer = generateRandomWord()
    known = len(answer) * '_'
    gameOver = False
    badGuessesLeft = 10
    badGuesses = set()
    while(not gameOver):
        print("Try a letter. The word is", len(answer), "letters long. Here's what we have so far: ", known)
        if len(badGuesses) > 0:
            print("Incorrect guesses: ", badGuesses)
        attempt = input().lower()
        res = parseGuess(attempt, answer, known, badGuessesLeft, badGuesses)
        if res[0] == "quit":
            # quit case
            return
        elif res[0] != "bad_input":
            known = res[0]
            correct = res[1]
            if not correct:
                badGuessesLeft -= 1
                badGuesses.add(attempt)
            if badGuessesLeft <= 0:
                gameOver = True
                print("You lose! You only got: ", known)
                print("Press 'c' to try again, or anything else to quit.")
                response = input()
                if response == 'c':
                    return gameRun()
            else:
                if known == answer:
                    gameOver = True
                    print("You win! The answer is", known)
                    print("Press 'c' to try again, or anything else to quit.")
                    response = input()
                    if response == 'c':
                        return gameRun()

def generateRandomWord():
    # unimplemented
    if len(listOfWords) > 0:
        return (random.choice(listOfWords).lower()).decode("utf-8")
    
def parseGuess(input, answer, known, badGuessesLeft, badGuesses):
    if input == '#q':
        print("Goodbye!")
        return "quit", True
    elif len(input) > 1 or len(input) < 1:
        print("--------------")
        print("You can only enter one letter at a time. Try again.")
        return "bad_input", True
    else:
        print("--------------")
        if input in answer:
            for i in range(len(answer)):
                if answer[i] == input:
                    tempList = list(known)
                    tempList[i] = input
                    known = ''.join(tempList)
            print("Good job! Remaining wrong guesses: ", badGuessesLeft)

            return (known, True)
        elif input in badGuesses:
            print("You already guessed this letter. Try again!")
            return (known, True)
        else:
            print("Letter not found! Remaining wrong guesses: ", badGuessesLeft - 1)
            return (known, False)

def parseStartInput(input):
    if input == '#q':
        print("Goodbye!")
    elif input == 'b' or input == 'B':
        keepPlaying = gameRun()
    else: 
        print("Read the instructions...")

def main():
    print(gameStartText)
    parseStartInput(input().lower())

if __name__=="__main__":
    main()