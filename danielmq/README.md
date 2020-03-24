
# OpenDNA
@author:  Daniel Martin Marin Quiroz
@version: Mar 12,  2020
@class: CS41

### Description

Hi there! This project is an attempt to build an interface that lets a user interact with a database of human profiles, each of which is consisted on the name of the human, her/his age and a part of her/his DNA sequence.

The user enters this information and the program compares his/her DNA against the current database of registered user profiles. After the algorithm computes the results, the user is shown the profiles of the people whose DNA is the most similar to his/hers. Also, by using the Needleman-Wunsch sequence alignment algorithm, the user is shown the best possible alignment of two DNA sequences.

The results are ranked by the similarity of the DNA sequences of each profile with the DNA of the user, and the alignments are highlighted by the program, indicating matches, mismatches and gaps in each alignment. Finally, the user is able to save her/his information in the database so that future users are able to compare their DNA sequences with her/him.

### How to run

This project was designed to run both locally and also using the website template posted on Piazza. To run locally, simply type `python openDNA.py`. This will create a radomly generated user profile, compare his/her DNA against a randomly generated user database of (by default) 100 users and display the matchings, rankings and results.

The program can be run with the following command-line arguments:  `python openDNA.py --randomDatabase` and `python openDNA.py --localDatabase`.
Both options let the user enter his/her information (name, age and DNA sequence). The first compares his/her DNA with a randomly generated database and the latter compares it with an actual file in the `data/` folder named `userDatabase.json`, and it lets the user save his/her profile in the database if he/she wishes to do so.

To run on the web, run `python app.py`. This will create a local server that can be accessed on a web browser. On this website, the user is able to enter his/her name, age and DNA sequence. The server will receive the request and confirm that the data entered is in the correct format. If it is the case, then the user will be able to see the rankings, best matchings and similarities of the profiles in the database at `data/userDatabase.json`, and her/his information will be added (or updated) to such database.

### Code design

Basically all the relevant code is on the `openDNA.py` file. My approach was to use Python's classes to create a `Person` class that holds the user's information and a `DNAComparison` class that is instantiated with two `Person` objects and holds data such as the best alignment of the two person's sequences, percent similarity and their relative Needleman-Wunsch similarity scores.

I also created functions that would be in charge of loading/saving into the user database, create random DNA sequences, create random user-profiles, verify the validity of the information entered by the user, process the online requests, run the comparison of one profile against the whole database of user, format the results and interact with the user when run locally.

### Credits
I have used the implementation of the Needleman-Wunsch algorithm coded by the Wilke Computational Evolutionary Biology Lab, from the class of Spring 2018 available at [this](https://wilkelab.org/classes/SDS348/2018_spring/labs/lab13-solution.html) link.

### Publishing
Feel free to publish/use anything from this project!

### Video
You can find the walkthrough video here: https://drive.google.com/open?id=1ukpae3Zmj4ylQvm3LzWjqdfVz7DG1zLc

