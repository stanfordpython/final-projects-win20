import time as t
import random as r

#TODO: High scores

class GameShow:
    def __init__(self):

        """
        These are the characters in the game show. host wil be populated
        randomly by one of the elements in possibleHosts. aud is the audience.
        """
        self.host = ""
        self.possibleHosts = ["STEVE HARVEY", "PAT SAJAK", "BARACK OBAMA",
                              "SNOOP DOGG", "ALEX TREBEK", "SETH ROGEN", "JOHN MULANEY",
                              "SHAWN MENDES", "CHARLIE PUTH", "DAVID DOBRIK", "LIZZO", "DOJA CAT",
                              "THE WEEKND", "POST MALONE"]
        self.aud = "AUDIENCE: "


        """
        agreeWds is a pseudo-NLP set of words. When asking a yes-or-no question in the game,
        all we need to do is search the user's response for any of the substrings below. For
        example, 'ye' catches the words yes, yeah, yeet, and so on.
        """
        self.agreeWds = ['ye', 'bet', 'def', 'sure', 'yup',
                      'ok', 'sounds good', 'tot', 'mhm', 'def', 'why',
                      'cert', 'course', 'yaa', 'd be', 'm be',
                      'gladly', 'indeed', 'undoubtedly', 'obvi', 'maybe',
                         'a doubt', 'oui', 'si','hai','aye','ya', 'guess']

        #Dialogue for the host to use to prompt the user for the next letter
        self.prompts = ["What'll your next guess be?", "Time to guess another letter:",
                        "What's up next?",
                        "What letter would you like next?",
                        "Alright, what's next? Remember, you can guess a letter or tell me 'solve' at any time, if you think you know the answer: ",
                        "It's time for your next letter. And don't forget, vowels cost you $200: ",
                        "What would you like your next letter to be? "]

        #Each of these variables keeps track of different things. Names should be self-explanatory
        self.numRounds = 3
        self.promptsLen = len(self.prompts)
        self.topicsDone = [] #List of topics already done this game, to avoid duplicates
        self.puzzles = {} #To be populated. Keys are topics, values are puzzles.
        self.topic = ""
        self.puzzle = ""
        self.cont = True
        self.board = ""
        self.borders = ""
        self.alreadyGuessed = [] #List of letters that the user already guessed
        self.score = 0
        self.bank = 0
        self.vowelCost = 200
        self.bankruptNum = -137

        #As of right now, chances of getting a bankrupt on a single spin is 1/6
        self.wheelValues = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000,
                            self.bankruptNum, self.bankruptNum, self.bankruptNum]
        self.spinVal = 0
        self.scoreFile = "scoreFile.txt"

    #Used for aesthetic purposes in the text interface
    def space(self):
        print("")

    #Used for giving the user time to read each line in the text interface
    def pz(self):
        t.sleep(1)

    #Returns whether or not the user responded affirmatively to a yes-or-no question
    #Pseudo-NLP
    def saysYes(self, r):
        for w in self.agreeWds:
            if w in r:
                return True
        return False

    #Starts the game. At first we ask the user what their name is, then we
    #ask them if they're ready to play. If so, we have an aesthetically pleasing
    #introduction to show, just like in real Wheel of Fortune.
    def startIntro(self):
        self.space()
        name = input(self.host + "Hey there, contestant! What's your name? ")
        while len(name) < 1:
            print(self.host + "Silence is not a name, buddy.")
            self.pz()
            print(self.aud + "*laughs*")
            self.pz()
            name = input(self.host + "What's your name? ")
        self.name = name[0].upper() + name[1:].lower()
        response = input(self.host + "Alright, " + self.name + ", are you ready to play? ")
    
        if response.lower() == 'y' or self.saysYes(response.lower()):
            print(self.host + "Then let's play...")
            t.sleep(0.75)
            self.space()
            print("*drumroll*")
            self.space()
            t.sleep(1.5)
            print(self.aud + "WHEEL!")
            t.sleep(1.0)
            print(self.aud + "OF!")
            t.sleep(1.0)
            print(self.aud + "FORTUNE!")
            t.sleep(1.0)
            self.space()
            print("*theme song plays*")
            self.space()
            t.sleep(1.0)
            print("############# WHEEL OF FORTUNE !!!! ############")
        else:
            self.cont = False
            print(self.host + "Maybe some other time then...")

    #Selects a puzzle from the dictionary of possible puzzles. Populates self.puzzle
    def pickAPuzzle(self):
        tops = self.puzzles.keys()
        lTops = list(tops)
        numTopics = len(tops)
        self.topic = lTops[r.randint(0, numTopics - 1)]

        #To avoid picking from the same topic twice.
        while self.topic in self.topicsDone:
            self.topic = lTops[r.randint(0, numTopics - 1)]

        self.topicsDone.append(self.topic)
        potentials = self.puzzles[self.topic]
        numPots = len(potentials)
        self.puzzle = potentials[r.randint(0, numPots - 1)]
        self.topic = self.topic.upper()
        self.puzzle = self.puzzle.upper()
        self.puzzle = self.puzzle[:-1]

    # We read all the possible puzzles from a file. That file is formatted as
    # TOPIC:PUZZLE, with one entry per line. We populate self.puzzles as we read this file
    def loadPuzzle(self, filename):
        with open(filename) as f:
            for line in f:
                if line == "\n":
                    pass
                else:
                    arr = line.split(':')
                    topic = arr[0]
                    puzz = arr[1]
                    topic = topic.upper()
                    puzz = puzz.upper()
                    if topic not in self.puzzles.keys():
                        self.puzzles[topic] = [puzz]
                    else:
                        self.puzzles[topic].append(puzz)
        self.pickAPuzzle()

    #Dialogue for the host to announce the category
    def setUpCategory(self):
        self.space()
        self.pz()
        print(self.host + "Alright, let's just jump into it.")
        self.pz()
        print(self.aud + "*applauds*")
        self.pz()
        print(self.host + "The category of our puzzle today is " + self.topic)
        self.pz()
        print(self.aud + "*cheers*")

    #Takes the puzzle for the user to solve and replaces it with a series of blanks, like hangman
    def initializeBoard(self):
        if(self.borders == ""):
            for i in range(50):
                self.borders += chr(9608)
        for ch in self.puzzle:
            if ch.isalpha():
                self.board += "_"
            else:
                self.board += ch

    #Aesthetically displays the puzzle to the user, just like the board in the show.
    #We also display the topic, the player's accumulated score (bank), and the player's
    #round earnings (score)
    def displayPuzzle(self):
        print(self.borders)
        self.space()
        print(self.board)
        self.space()
        print(self.borders)
        print("Topic: " + self.topic)
        print("Bank: $" + str(self.bank))
        print("Score: $" + str(self.score))
        self.space()

    #Randomly chooses a phrase for the host to say to prompt the player for another letter
    #This functionality is purely for entertainment purposes
    def readNextPrompt(self):
        num = r.randint(0, self.promptsLen - 1)
        guess = input(self.host + self.prompts[num] + " ")
        return guess

    # After each letter the player guesses, we update the puzzle board.
    # If the letter appears in the puzzle, we fill in those blanks and redisplay the puzzle
    # Otherwise, we inform the user their guess was wrong.
    # No money is lost for wrong guesses. However, if the user guesses correctly,
    # their round socre increases by the wheel's spin value multiplied by the frequency
    # of that letter in the puzzle. For example, if the wheel lands on $500 and the user
    # guesses the letter "P". If "P" appears twice in the puzzle, then the user just earned $1000.
    def updatePuzzleAndScore(self, guess):
        inds = []
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == guess:
                inds.append(i)
        if len(inds) == 1:
            print(self.host + "One " + guess)
        else:
            print(self.host + "There are " + str(len(inds)) + " " + guess + "\'s")
        self.pz()
        print(self.aud + "*cheers*")
        s = list(self.board)
        for nd in inds:
            s[nd] = guess
        self.board = "".join(s)
        self.pz()
        self.score += len(inds) * self.spinVal

    #If the user guesses the same letter twice in the same round, we laugh at them
    def alreadyGuessedDialogue(self, guess):
        print(self.host + self.name + " you've already guessed " + guess)
        self.pz()
        print(self.aud + "*laughs*")
        self.pz()
        print(self.host + "Okay, guys, let's settle down. " + self.name + ", why don't you try again?")
        self.pz()

    #If the user guesses a letter incorrectly, this dialogue appears
    def wrongGuessDialogue(self, guess):
        print(self.host + "No " + guess + "\'s.")
        self.pz()
        print(self.aud + "Awww")
        self.pz()

    #If the user indicates they want to guess what the puzzle is, we say this
    def letUserSolvePuzzle(self):
        print(self.host + "Oh, you want to solve the puzzle?")
        self.pz()
        print(self.aud + "Ooooohh")
        self.pz()
        soln = input(self.host + "Okay, " + self.name + ", go ahead and solve the puzzle: ")
        soln = soln.upper()
        return soln

    #Prompts the user to guess a letter
    def getGuess(self, isFirstTime):
        guess = ""
        if(isFirstTime):
            guess = input(self.host + "Okay, " + self.name + ", what's your first letter? ")
        else:
            guess = self.readNextPrompt()
        return guess

    # If the user solves the puzzle as a whole, this is how we check if their guess is right.
    # If the user writes spaces instead of dashes, it doesn't matter. So if the puzzle is
    # "LEFT-HAND TURN", then we'll accept "LEFT HAND TURN" and "LEFT-HAND TURN" as correct.
    def checkAlphaMatch(self, soln):
        soln = soln.strip()
        if len(soln) == len(self.puzzle):
            for i in range(len(soln)):
                if self.puzzle[i].isalpha():
                    if soln[i] != self.puzzle[i]:
                        return False
        else:
            return False
        return True

    #Wrapper: if the user wants to solve the puzzle, this checks their solution.
    def checkSoln(self):
         soln = self.letUserSolvePuzzle()
         soln = soln.upper()
         return self.checkAlphaMatch(soln)

    #If the user's attempt to solve the puzzle was wrong, this dialogue appears
    def missedSolnDialogue(self):
        print(self.host + "Oof, that doesn't seem to be the right answer.")
        self.pz()
        print(self.aud + "Awwww")
        self.pz()

    #Updates the user's score for a given round after each guess
    def updateScoreForSolve(self):
        mult = 0
        for ch in self.board:
            if ch == "_":
                mult += 1
        self.score += (mult * self.spinVal)

    #Just like the show, guessing a vowel costs $200. If the user guesses a vowel, this
    #dialogue appears, and we adjust the globals accordingly
    def buyAVowel(self, guess):
        if guess in "AEIOU":
            print(self.host + "Okay, you guessed a vowel, so that costs you $" + str(self.vowelCost))
            self.pz()
            self.score -= self.vowelCost

    #Function that prompts the user for letter guesses. We do some input checking so that guesses
    #must be one alphabetic character. Or the user can say they want to "solve", in which case
    #we ask for their solution to the puzzle. We also check if the user made a duplicate guess
    def askForLetters(self, isFirstTime):
        guess = ""
        self.pz()
        guess = self.getGuess(isFirstTime)
        if "solve" in guess.lower():
            correct = self.checkSoln()
            if correct:
                print(self.host + "That is correct!")
                self.pz()
                print(self.aud + "*Applause*")
                self.pz()
                self.updateScoreForSolve()
                self.board = self.puzzle
                return
            else:
                self.missedSolnDialogue()
                guess = input(self.host + "Why don't you try and guess a letter? ")
        while(True):
            if(len(guess) != 1):
                guess = input(self.host + "You can only guess one letter: ")
            elif(not guess[0].isalpha()):
                print(self.host + "That's not a letter, bud")
                self.pz()
                print(self.aud + "*laughs*")
                self.pz()
                guess = input(self.host + "Let's try to guess a letter this time: ")
            else:
                break
        guess = guess.upper()
        if guess in self.alreadyGuessed:
            self.alreadyGuessedDialogue(guess)
        elif guess in self.puzzle:
            self.buyAVowel(guess)
            self.updatePuzzleAndScore(guess)
        else:
            self.buyAVowel(guess)
            self.wrongGuessDialogue(guess)
        self.alreadyGuessed.append(guess)

    #Dialogue to announce what round it is. The first and last rounds get special dialogue.
    def roundNumDialogue(self, i):
        if i == 0:
            print(self.host + "Alright, it's time for our first round.")
        elif i == self.numRounds - 1:
            print(self.host + "Okay, this is the final round. Let's end with a bang.")
        else:
            print(self.host + "It's time for the next round. Here we go!")
        self.pz()

    #In between rounds, we reset the board to have a bunch of blanks, we reset the 
    #alreadyGuessed letters list to be empty, whatever the user earned in the previous
    #round to their bank, we reset the round score to zero, and we display a new puzzle.
    def resetBoard(self):
        self.board = ""
        self.alreadyGuessed = []
        self.bank += self.score
        self.score = 0
        self.pickAPuzzle()
        self.initializeBoard()

    #More dialogue in between rounds
    def betweenRoundDialogue(self):
        self.pz()
        print(self.host + "Alright, it looks like it's time for the next round!")
        self.pz()
        print(self.aud + "*cheers*")
        self.pz()
        print(self.host + "Okay, let's reset the board and see the new puzzle!")
        self.pz()

    #The wheel itself spins, and we wait for a random amount of time between 1 and 6 seconds
    #for dramatic tension
    def spinDialogue(self):
        print("*wheel spins*")
        num = r.randint(1, 6)
        for i in range(num):
            print("...")
            self.pz()
        print("*wheel stops*")
        self.pz()

    #If the wheel lands on BANKRUPT, this is the dialogue
    def bankruptDialogue(self):
        self.pz()
        print(self.host + "Oh no! It seems like the wheel has landed on BANKRUPT")
        self.pz()
        print(self.aud + "Booooo")
        self.pz()
        print(self.host + "I'm sorry, " + self.name + ". You've just lost all your money.")
        self.pz()
        print(self.aud + "*Boos louder*")
        self.pz()
        print(self.host + "Don't worry. Let's try to earn that money back.")
        self.pz()
        print(self.host + "Spin the wheel again!")
        self.pz()

    # We spin the wheel by randomly picking a number from wheelValues. This random number
    # is how much the user's guess is worth. However, as of the submission
    # of this assignment, there is a 1/6 chance of bankrupting, meaning all the user's
    # earnings for this round drop to zero.
    def spinTheWheel(self):
        self.pz()
        print(self.host + "Okay, let's spin the wheel to see how much your next guess is worth")
        self.pz()
        self.spinDialogue()
        val = self.wheelValues[r.randint(0, len(self.wheelValues) - 1)]
        if val == self.bankruptNum:
            self.score = 0
            self.spinVal = 0
            print("WHEEL: BANKRUPT")
            self.bankruptDialogue()
            self.spinTheWheel()
        else:
            print("WHEEL: $" + str(val))
            self.pz()
            print(self.host + "Okay, it looks like your next guess is worth $" + str(val) + " per letter.")
            self.spinVal = val
            self.pz()

    # A short spiel at the beginning of the game to teach new users how to play.
    def miniTutorial(self):
        self.pz()
        self.pz()
        print("")
        print(self.host + "Okay, don't forget. Your goal is to earn as much money as possible")
        t.sleep(1.5)
        print(self.host + "Every correct guess earns you more money.")
        self.pz()
        print(self.host + "The more frequently the letter appears in the puzzle, the more money your earn.")
        t.sleep(1.5)
        print(self.host + "Vowels cost $" + str(self.vowelCost))
        self.pz()
        print(self.host + "And don't forget, the wheel can land on \'BANKRUPT\' at any time")
        self.pz()
        print(self.aud + "Ooooh")
        self.pz()
        print(self.host + "So, it's in your best interest to guess the puzzle as quickly as possible.")
        self.pz()
        print(self.aud + "*cheers*")
        print("")
        self.pz()
        self.pz()

    #Starts off the game with dialogue and continues for numRounds number of rounds.
    def playGame(self):
        self.setUpCategory()
        self.initializeBoard()
        self.miniTutorial()
        self.pz()
        print(self.host + "Okay, let's put the puzzle up on the board")
        self.space()
        self.pz()
        isFirstTime = True
        for i in range(self.numRounds):
            #print(self.puzzle)
            self.displayPuzzle()
            self.roundNumDialogue(i)

            #While the puzzle hasn't yet been fully guessed, spin the wheel and prompt the user
            while("_" in self.board):
                self.spinTheWheel()
                self.askForLetters(isFirstTime)
                isFirstTime = False
                self.displayPuzzle()
                
            #The round is done once the puzzle is fully guessed, so we reset the board
            self.resetBoard()
            if i < self.numRounds - 1:
                self.betweenRoundDialogue()

    #This is just for fun. We randomly pick a host.
    def pickHost(self):
        n = r.randint(0, len(self.possibleHosts) - 1)
        self.host = self.possibleHosts[n] + ": "

    #At the end of the game, we update the leaderboard in a separate file.
    def updateLeaderboard(self, scores):
        scores.append((self.name, self.bank))
        scores = sorted(scores, key = lambda x : x[1], reverse=True)
        scores = scores[0:3]
        with open(self.scoreFile, "w") as f:
            f.truncate(0)
            for s in scores:
                f.write(s[0] + ":" + str(s[1]) + "\n")
                print(s[0] + " " + str(s[1]))
        
    #Updates and prints the leaderboard (top 3 high scores, kept track of in a separate file)
    def printHighScores(self):
        #Format of self.scoreFile is NAME:SCORE
        scores = []
        print("LEADERBOARD: ")
        with open(self.scoreFile) as f:
            for line in f:
                arr = line.split(":")
                name = arr[0]
                score = arr[1]
                scores.append((name, int(score)))
        self.updateLeaderboard(scores)

                
                
        
###########################################################################################
###########################################################################################
########################## GAME SHOW CLASS ENDS HERE ######################################
###########################################################################################
###########################################################################################

#Main method. Self explanatory.
def main():
    gs = GameShow()
    gs.pickHost()
    gs.startIntro()
    if gs.cont:
        gs.loadPuzzle("puzzles.txt")
        gs.playGame()
        print("Congratulations! You've won...")
        t.sleep(1.5)
        print("WHEEL!")
        t.sleep(1.0)
        print("OF!")
        t.sleep(1.0)
        print("FORTUNE!")
        print("")
        gs.printHighScores()

main()

#If this comment is not on line 532, the file has been edited!
