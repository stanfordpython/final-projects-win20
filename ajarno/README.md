Final Project: TweetInsight - Twitter Analytics Tool
Name: AJ Arnolie
Date: 3/10/20
SUNet: ajarno
------------------------------------------------------------------------------------
Project Overview:
-----------------
This program is a Twitter scraper and analyzer that allows users to search for and 
recieve data for tweets based on either user or keyword. This data is then cleaned 
and analyzed for features such as average length, average like count, and commonly 
used words among many other features. These features, along with information about 
the selected user or keyword are printed to the screen. Next, sentiment analysis is 
performed on a random sample of tweets from the tweets produced by the users 
initial query. This sentiment analysis is performed using NLTK and a Naive-Bayes 
Classification Model that was implemented and trained previously. This model was 
trained on 10,000 pre-labeled tweets labeled positive or negative for sentiment and 
then this model was saved as a pickle file to be reloaded at the start of every 
program run. This removes the need to retrain the model every run. The results of 
the sentiment analysis on these tweets using the trained model is printed to the
screen, and an overall evaluation of the sentiment for the tweets from the selected
user or keyword is given. The program has the addition capability of allowing users
to type their own tweets to be evaluated using the sentiment analysis model. Finally, 
the user has the opportunity to re-query or exit the program. 

------------------------------------------------------------------------------------
Libraries Used:
---------------
Twitterscraper      - Used to scrape Tweets from Twitter based on user query inputs

NLTK                - Used to train the Naive-Bayes Classification model and to 
                      classify the downloaded Tweets afterward

Regular Expressions - Used to clean up tweets, removing urls and @'s for data analysis

Pickle              - Used to store and load the trained classification model

Itertools           - Used to manipulate lists in initial data analysis

Datetime            - Used to set the time range on the queries

String 		    - Used to eliminate punctuation tokens from the data to better 
                      prepare it for training and analysis

Random              - Used to scramble data for random samples

Logging 	    - Used to disable the info logs of the twitterscraper library

Collections         - Used to find the most common words present in the data

------------------------------------------------------------------------------------
Technical Code Overview:
------------------------
Modules:
 - tweet_insight.py
 - model_builder.py

There is the main file called tweet_insight, which holds the main function and many
of the functions for scraping tweets, formatting data, and performing analysis, and
then there is one additional module called model_builder.py, which both creates and
trains the Naive-Bayes Classification Model that is used for sentiment analysis as
well as for performs sentiment analysis on the tweets that are scraped and compiled
in the main file.

tweet_insight.py:
----------------
This file is the main module for the program and holds the main function as well as 
many of the files that perform functions of scraping, formatting, and analyzing for 
the program as well as for the displaying of the program in the terminal.

disable_logger():
 - This functions purpose is to temporarily silence the constant info log prints
   from the twitterscraper library so that the programs visual aspect can be seen.

twt_print():
 - This function helps format the longer tweets in a way that is more visually appealing
   for displaying in the terminal. This includes newlines at 75 character intervals to
   prevent wrapping.

welcome_printout():
 - This function prints out the welcome message and instructions for the program.

get_user_input():
 - This function gets the users input for input type and input value. If the user types
   "q" at this point, the program is exited. If the user inputs an invalid input type
   or an invalid input, the user is prompted to input a valid input. After all of the 
   data is collected, it is returned by the function to be used in following functions.

scrape_tweets():
 - This function is responsible for performing queries to the twitterscraper library
   based on the inputs of the user in the previous function. If the user selects "user"
   as input type, the function searches for tweets from the user that was chosen. If the
   user selects "keyword", the function searches for tweets containing that keyword from
   the last 2 week. The returned tweets are then returned by the function to be formatted
   and analyzed.

format_data():
 - This function takes the returned tweets and formats them in order to make some of the
   basic analysis easier. This includes ensuring that there are no retweets included, making
   sure that the keyword actually appears in the tweet as well as using regular expressions
   to remove any @usernames or http links from the tweets and confirming that the tweet is not
   empty. The function then returns the list of edited tweets

find_freq_words():
 - This function takes the output of the previous function and uses it to determine the most
   frequent words that appear in the tweets. The function tokenizes the tweets, removes all
   non alphabetic tokens and stop words, and then uses collections.Counter() to determine the
   10 most frequent words.

start_data_analysis():
 - This function performs the bulk of the data analysis based on the data cleaned by previous
   functions. It takes the tweets and collects data for things such as longest/shortest tweet,
   most liked/retweeted tweet, etc. This function then compiles these categories and results
   to a dictionary for easier printing in the main function.

main():
 - This function calls all of the other functions defined in the projects and handles the loop
   for the program. The main function first calls the functions for logger handling, downloading,
   and printing the welcome message. It then starts the loop and prompts the user for input. If 
   the user wants to type their own tweet, the function performs sentiment analysis on that tweet.
   Otherwise, it takes this input and passes it into the relevant functions for formatting, cleaning,
   and analyzing. The results of both the basic and sentiment analyses are printed out to the screen
   and the loop starts again. This loop is exited when the user types "q". 

model_builder.py:
-----------------
This module is a helper module that handles all the functions of the program that
are related to the training or use of the sentiment analysis model. Functions from
this file are imported and used in the main module of the program.

download_nltk_packages():
 - This function is responsible for downloading the resources from NLTK necessary
   to create and use the classification model. This includes punkt, a sentence
   tokenizer, average_perceptron_tracker a POS word tagger, wordnet which helps
   with lemmatizing words, and stopwords, a database of words to remove before 
   analysis. These downloads are used in later functions.

clean_training_data():
 - This function is the first step in accessing and formatting the sample data from
   NLTK that is used to train the model on. This function tokenizes, cleans, and
   formats the data from the .json files using numerous list comprehension and filter
   functions. After both the samples for the positive and negative tweets are cleaned
   and formatted, the data for these two sets are shuffled and returned for training.

clean():
 - This function performs much of the cleaning for the previous function. This function
   removes punctuation tokens, @usernames, http links, stop words, and empty tokens. It
   also labels each token by part of speech and then lemmatizes each based on this. 
   Finally, every token is made to be lower case and then is retured as a list. This 
   function is called on each individual tokenized tweet for both data sets.

save_classifier_model():
 - This function makes use of pickle to save the trained classifier model so that these
   functions don't have to be run every time the program is executed.

build_model():
 - This acts as a main function for this module in that it calls many of the other
   functions to complete the building and training process. This function downloads the
   packages, creates the classifier, trains it, and then tests its accuracy, finally
   saving the classifier and exiting.

determine_sentiment():
 - This is a helper function that is used to determine the overall sentiment of a 
   query based on the number of positive and negative sentiments that were found from
   a random sample of tweets based on the query. This function provides a printout
   for different percentages of positive to negative classifications ranging from 
   "Very Positive" to "Very Negative".

perform_sentiment_analysis():
 - This function is the function that is used to classify the random sample of tweets
   described above. The function downloads the model from the pickle file and then 
   uses the model to classify at most 50 of the loaded tweets. It takes these tweets,
   tokenizes and cleans them and then classifies them as positive or negative. These
   results as well as the overall sentiment calculated in the function above are then
   printed to the screen.

------------------------------------------------------------------------------------
Requirements to Run:
--------------------
- A stable internet connection
- Must be running Python 3 (I have version 3.8.0)

------------------------------------------------------------------------------------
Installation Instructions:
--------------------------
- Download the files provided in the submission. These should include the main Python
  file (tweet_insight.py), the model module (model_builder.py), the saved classifier 
  (classifier.pickle), the readme file (README.md), and the requirements file 
  (requirements.txt). Make sure that everything is in the same location!

- Ensure that twitterscraper, nltk, and all relevant libraries are installed. This can
  be handled by running 'pip install -r requirements.txt' on the requirements file
  included in the submission or by individual installation.

- Make sure an internet connection has been established. The twitterscraper will not
  be able to pull Tweets from Twitter otherwise.

- Compile and run the main file tweet_insight.py in order to start the program

- If you would like to retrain the classifier, simply uncomment the build_model
  function included in the main function. This will overwrite the previously saved
  classifier with a newly trained classifier and then exit the program.
------------------------------------------------------------------------------------
Known Bugs:
-----------
When the user is not connected to the internet, the program will crash immediately
after being run. This is because the twitterscraper library needs an internet connection
in order to pull Tweets from the internet.

Additionally, on very rare occasions, the program crashes because of errors having to do 
with fork management within the twitterscraper library. I've attempted to make changes to
solve this problem, but I believe it is just a minor limitation of the twitterscraper 
library. The easiest fix to this problem is simply to restart the program.

Something that is not a bug but still is something that I though I should address is
the accuracy of the classification model. From tweet to tweet, it doesn't perform perfectly, 
(though it is more accurate than I anticipated) but it does a fairly good job of getting 
the overall sentiment of a bunch of tweets from a query. For example, searching the keywords 
'happy' and 'sad' will give very clear '+' and '-' responses, though not every individual 
Tweet is necessarily classified correctly. The model cannot determine sarcasm and doesn't 
have any context for its classifications, so it cannot possibly be perfect.
------------------------------------------------------------------------------------
Credits:
--------
Twitterscraper - Ahmet Taspinart (aspinar@gmail.com)

NLTK (Natural Language Toolkit) - Team NLTK (www.nltk.org)
      Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing 
      with Python. O’Reilly Media Inc.
      - The NLTK documentation and website were extremely helpful in guiding me 
         through selecting data and formatting it correctly for training on the model.


       A special thanks to Parth Sarin, Michael Cooper, and Sam Kwong for 
       their help with this project and throughout the rest of the course!

------------------------------------------------------------------------------------
Contact Information:
--------------------

				Name: AJ Arnolie
			   Email: ajarno@stanford.edu

------------------------------------------------------------------------------------

         I'm comfortable with this project being published if necessary.

------------------------------------------------------------------------------------