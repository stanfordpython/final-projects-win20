'''
    main.py
    @author:    Daniel Martin Marin Quiroz
    @version:   March 11, 2020
    @class:     CS41

    This file implements a DNA ranking system that lets users compare their
    own DNA sequence against a database of registered users. It uses the
    Needleman-Wunsch algorithm to calculate the best pairwise alignement of two
    DNA sequences, which is shown to the user. This comparison is made for
    every user in the database, also calculating the similarity bewteen two
    DNA strands. Finally, the results are ranked and the user is shown a list
    of the registered users with the most similar DNA sequences, as well as
    the best alignment found by the Needleman-Wunsch algorithm.
    
'''
import sys
import random
import json
from NeedlemanWunsch import needleman_wunsch

LETTERS = 'ATGC'
MUTATION_PROBABILITY = 0.5
DEFAULT_NUM_USERS = 100
DEFAULT_DNA_LENGTH = 70
DATABASE = "data/userDatabase.json"
FIRST_NAMES_ADDRESS = "data/names.txt"
SURNAMES_ADDRESS = "data/surnames.txt"


class Person:
    def __init__(self, name, dna, age):
        self.name = name
        self.dna = dna
        self.age = age

    def __str__(self):
        str = ""
        str += "\nUser created:\n"
        str += f"\n\tname \t= {self.name}\n"
        str += f"\tage \t= {self.age}\n"
        str += f"\tDNA \t= {self.dna}\n"
        return str


class DNAComparison:
    def __init__(self, person1, person2):
        self.person1 = person1
        self.person2 = person2
        self.str1, self.str2, self.score = needleman_wunsch(person1.dna, person2.dna)
        self.similarity = self.getSimilarity(self.str1, self.str2)

    @staticmethod
    def getSimilarity(str1, str2):
        '''Computes the similarity as percentage of the number of alignments in
        two processed DNA sequences.'''
        count = 0
        for i in range(len(str1)):
            if str1[i] == str2[i]:
                count += 1
        return (count / len(str1)) * 100

    @staticmethod
    def getMatchingLines(str1, str2):
        '''Analyzes two processed DNA sequences and generates a string that shows
        for each position in the strings whether the sequences match, mismatch or
        if there is a gap.
        '''
        matchingLines = ""
        for i in range(len(str1)):
            if str1[i] == str2[i]:
                matchingLines += '|'
            elif str1[i] != str2[i] and str1[i] != '-' and str2[i] != '-':
                matchingLines += ':'
            else:
                matchingLines += ' '
        return matchingLines

    def displayAlignment(self):
        '''Returns a formatted version of the matching between the two sequences'''
        result = ""
        matchingLines = self.getMatchingLines(self.str1, self.str2)
        result += "\tDNA1:\t\t" + self.str1 + "\n"
        result += "\t    \t\t" + matchingLines + "\n"
        result += "\tDNA2:\t\t" + self.str2 + "\n"
        result += "\tScore:\t\t" + str(self.score) + "\n"
        result += "\tSimilarity:\t{0:2.2f}%\n".format(self.similarity)
        return result


def randomDNA(length):
    '''Returns a random DNA sequence'''
    result = ""
    for _ in range(length):
        result += random.choice(list(LETTERS))
    return result


def randomMutation(originalDNA, probability):
    '''Returns a mutated version of the original DNA sequence with
    a given probability of mutation for each character'''
    result = ""
    for i in range(len(originalDNA)):
        if random.random() < probability:
            result += random.choice(list(LETTERS))
        else:
            result += originalDNA[i]
    return result


def generateRandomProfiles(num, sample):
    '''
    Generates 'num' random Person objects with DNA mutations based on the sample 'sample'
    '''
    with open(FIRST_NAMES_ADDRESS) as file:
        firstNames = file.read().splitlines()
    with open(SURNAMES_ADDRESS) as file:
        surnames = file.read().splitlines()

    randomProfiles = []
    for _ in range(num):
        attributes = {}
        attributes['dna'] = randomMutation(sample, MUTATION_PROBABILITY)
        attributes['age'] = random.randint(1, 100)
        attributes['name'] = random.choice(
            firstNames) + " " + random.choice(surnames)
        randomProfiles += [Person(**attributes)]
    return randomProfiles


def saveProfiles(profiles, filename):
    '''Saves the list of Person objects in "profiles" as dictionaries in json
    format in the file "filename"'''
    profiles = [person.__dict__ for person in profiles]
    with open(filename, 'w') as file:
        json.dump(profiles, file, sort_keys=True, indent=4)


def saveUser(profiles, user, filename):
    '''Adds a user to the database'''
    profiles = [person.__dict__ for person in profiles]
    for dict in profiles:
        if dict['name'] == user.name:
            profiles.remove(dict)
    profiles += [user.__dict__]
    with open(filename, 'w') as file:
        json.dump(profiles, file, sort_keys=True, indent=4)


def loadProfiles(filename):
    '''Returns a list of users from the database pointed to by "filename".'''
    with open(filename, 'r') as file:
        profilesAsDicts = json.load(file)
    return [Person(**d) for d in profilesAsDicts]


def compareWithAllUsers(user, allUsers):
    '''Compares a user's DNA with the DNA sequences of all the profiles in "allUsers".'''
    comparisons = [DNAComparison(user, person) for person in allUsers]
    return sorted(comparisons, key=lambda x: x.similarity, reverse=True)


def validate_DNA(dna):
    '''Determines whether or not a DNA sequence is valid.'''
    for ch in dna:
        if ch not in LETTERS:
            return False
    return True


def loadDNA(filename):
    '''Returns the contents of a file as a string. Does not check if DNA is valid, to do so
    see validate_DNA() above.'''
    with open(filename, 'r') as f:
        dna = f.read()
    return dna


def promptUserForInfo():
    '''Retrieves sufficient valid information from the user as input to the console
    that allows for the creation of a valid Person object'''
    name = input("Enter your name: ")
    while True:
        try:
            age = int(input("Enter your age: "))
            if age >= 0 and age <= 150:
                break
            print("Please enter an age between 0 and 150.")
        except ValueError:
            print("Please enter an integer number")
    while True:
        print("Please enter your DNA. Press (r) for random or (f) to load from file.")
        response = input("Enter your DNA: ")
        if response.strip().lower() == 'r':
            dna = randomDNA(80)
            break
        elif response.strip().lower() == 'f':
            filename = input("Enter the address of the file: ")
            try:
                response = loadDNA(filename)
            except BaseException:
                print("Could not read file. Please try again.")
                continue

        if validate_DNA(response):
            dna = response
            break
        else:
            print("Invalid DNA format. Please try again.")

    return Person(name, dna, age)


def resultsToStrings(results):
    '''Returns a list of formatted strings containing the result of every comparison and
    their position in the ranking'''
    result = []
    for i, DNAComparison in enumerate(results):
        str = "{} Comparing {} with {}:\n".format(
            i + 1, DNAComparison.person1.name, DNAComparison.person2.name)
        str += DNAComparison.displayAlignment() + '\n'
        result += [str]
    return result


def runRandomDNAComparison(user):
    '''Compares the user's DNA sequence against a randomly generated database of user profiles'''
    profiles = generateRandomProfiles(DEFAULT_NUM_USERS, user.dna)
    results = compareWithAllUsers(user, profiles)
    return resultsToStrings(results)


def runDNAComparison(user, save=True):
    '''Compares the user's DNA sequence against the local database and optionally saves
    the user's info'''
    profiles = loadProfiles(DATABASE)
    str = ""
    results = compareWithAllUsers(user, profiles)
    message = resultsToStrings(results)
    if save:
        saveUser(profiles, user, DATABASE)
        str += f"The user \"{user.name}\" was successfully saved into the database.\n\n"
        message.insert(0, str)
    return message


def randomRun(DNALength):
    '''Creates a random user and compares his/her DNA against a randomly created database of users'''
    dna = randomDNA(DNALength)
    user = generateRandomProfiles(1, dna)[0]
    results = runRandomDNAComparison(user)
    print(user)
    printResults(results)


def printResults(results):
    '''Prints the list of string results in "results", letting the user control how
    much results to see'''
    print("\n\t\t\t--------Results of comparison with user database-------\n")
    for i in range(0, len(results)):
        print(results[i])
        if (i + 1) % 5 == 0 and i != len(results) - 1:
            usr_response = input(
                "Hit enter to see more results, or anything else to quit: ")
            print()
            if usr_response != "":
                break


def printHelp():
    '''Prints a helping message to the user if she/he does not supply a proper argument
    to the python script or if the argument is "---help".'''
    print("\nRun with the following options:\n")
    print("\t<empty>  \t\t creates a random user and compares it with a randomly created database")
    print("\t--debug  \t\t use predetermined seed to debug")
    print("""\t--localDatabase \t the user is asked to enter information, DNA is compared with local database\n \t\t\t\t and the users info is saved""")
    print("\t--randomDatabase \t the user is asked to enter information, DNA is compared with randomly created database")
    print()


def welcomeASCII():
    '''This one is pretty much self explanatory'''
    str = """
    

                ||        ______   .______    _______ .__   __.         _______  .__   __.      ___           ||
                ||       /  __  \  |   _  \  |   ____||  \ |  |        |       \ |  \ |  |     /   \          ||
                ||      |  |  |  | |  |_)  | |  |__   |   \|  |  ______|  .--.  ||   \|  |    /  ^  \         ||
                ||      |  |  |  | |   ___/  |   __|  |  . `  | |______|  |  |  ||  . `  |   /  /_\  \        ||
                ||      |  `--'  | |  |      |  |____ |  |\   |        |  '--'  ||  |\   |  /  _____  \       ||
                ||       \______/  | _|      |_______||__| \__|        |_______/ |__| \__| /__/     \__\      ||
                                                                                             
    """
    return str
    
def welcomeStr():
    '''Prints a welcoming message to the user'''
    str = """
    
                Welcome to OpenDNA. This program lets you compare your DNA with other users in the database.
                We'll tell you whose DNA is more similar to yours!!
            
    """
    return str


def getYesOrNo(prompt):
    '''Repeatedly asks the user for a yes or no answer'''
    while True:
        response = input(prompt)
        if response != "" and response.lower().strip()[0] == 'y':
            return True
        elif response != "" and response.lower().strip()[0] == 'n':
            return False
        else:
            print("Please enter yes or no.")


def main():
    '''Handles all the command-line argument parsing, creates the user and runs the
    comparison against the database'''
    print(welcomeASCII())
    print(welcomeStr())
    if len(sys.argv) == 1:
        randomRun(DEFAULT_DNA_LENGTH)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--debug':
            random.seed(0)
            randomRun(DEFAULT_DNA_LENGTH)
        elif sys.argv[1] == '--randomDatabase':
            user = promptUserForInfo()
            print(user)
            printResults(runRandomDNAComparison(user))
        elif sys.argv[1] == '--localDatabase':
            user = promptUserForInfo()
            print(user)
            if getYesOrNo("Would you like to save the user? "):
                printResults(runDNAComparison(user))
            else:
                printResults(runDNAComparison(user, False))
        else:
            printHelp()
    else:
        printHelp()


def processServerInput(name, dna, age, save):
    '''Handles web requests, determines if the user's input is valid and if it is the case,
    it returns the final ranking, matching and similarities as a formatted string.'''
    try:
        age = int(age)
    except BaseException:
        return "Please enter an integer for your age."
    if age > 150 or age < 0:
        return "Please enter an age between 0 and 150"
    dna = dna.upper()
    if not validate_DNA(dna):
        return "Please enter a valid DNA sequence. Only the letters ACGT are allowed."
    user = Person(name, dna, age)
    results = [welcomeASCII()]
    results += [str(user) + '\n']
    results += ["\n\t\t\t\t--------Results of comparison with user database-------\n"]
    results += runDNAComparison(user, save=save == 'Yes')
    finalString = ""
    for strLine in results:
        finalString += strLine
    return finalString


if __name__ == '__main__':
    main()
