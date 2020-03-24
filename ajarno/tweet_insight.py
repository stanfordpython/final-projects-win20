#!/usr/bin/env python3
"""Final Project: TweetInsight - Twitter Analytics Tool (main file)
Name: AJ Arnolie
Date: 3/10/20
SUNet: ajarno
----------------------------------------------------------------------------
This program is a Twitter scraper and analyzer that allows users to search
for and recieve data for tweets based on either user or keyword. This data
is then cleaned and analyzed for features such as average length, average
like count, and commonly used words among many other features. These
features, along with information about the selected user or keyword are
printed to the screen. Next, sentiment analysis is performed on a random
sample of 50 tweets from the tweets produced by the users initial query.
This sentiment analysis is performed using NLTK and a Naive-Bayes
Classification Model that was implemented and trained previously. This model
was trained on 10,000 pre-labeled tweets labeled positive or negative for
sentiment and then this model was saved as a pickle file to be reloaded at
the start of every program run. This removes the need to retrain the model
every run. The results of the sentiment analysis on these 50 tweets using
the trained model is printed to the screen, and an overall evaluation of
the sentiment for the tweets from the selected user or keyword is given. The
program has the additional capability of allowing users to type their own
tweets to be evaluated using the sentiment analysis model. Finally, the user
has the opportunity to re-query or exit the program.
----------------------------------------------------------------------------
"""

# Imports for Various Libraries used in Program
import re
import pickle
import nltk as n
from nltk.tokenize import word_tokenize
import itertools as it
import twitterscraper as ts
import datetime as dt
import string
import random
import logging
import collections as c

import model_builder as m


def disable_logger(b):
    """
    Disables the automatic info log outputs that the twitterscraper library
    uses for sake of program visuals.
    Arguments: b - boolean for if logger should be disabled
    Returns: N/A
    """
    if b:
        logger = logging.getLogger('twitterscraper')
        logger.disabled = True


def twt_print(data):
    data = str(data)
    for i in range(0, len(data), 75):
        if i == 0:
            print("{}".format(data[i:i+75]))
        else:
            print("\t    {}".format(data[i:i+75]))


def welcome_printout():
    """
    Prints out the welcome header and information for the program
    Arguments: N/A
    Returns: N/A
    """
    print("\n\n\t{}\n".format("----"*16))
    print("\t\t\t     Welcome to TweetInsight\n")
    print("\t\t     A Twitter Analytics Tool By: AJ Arnolie\n")
    print("\t{}\n".format("----"*16))
    print("\tIn this program, you can search for tweets from a specific")
    print("\tuser OR with a specific keyword in order to see statistics")
    print("\tabout those tweets. The program will then show you a sentiment")
    print("\tanalysis for 50 of these tweets and an overall sentiment")
    print("\tanalysis of the user or keyword based on that sample. Try")
    print("\tsearching with a sentiment based keyword like 'glad' or 'sad'")
    print("\tto see if the model can detect it, or just search for your")
    print("\tfavorite Twitter user. Finally, you have the option to type")
    print("\t     your own tweet to analyze for sentiment. Enjoy!\n\n")


def get_user_input():
    """
    Prompts the user for input in terms of an input type and search input.
    The program returns these two values for use in later functions.
    Arguments: N/A
    Returns: user-inputted value and type of that input
    """
    i_type = ""
    while i_type.lower() not in ["keyword", "user", "tweet", "q"]:
        print("\tWould you like tweets from a specific user OR keyword?")
        print("\tWould you like to create your own tweet?")
        print("\tType 'user', 'keyword', or 'tweet' to make a selection.")
        i_type = input("\tOr, type 'q' to exit: ")
    if i_type.lower() == "q":
        print("\n\tThank you for using Tweet Analyzer. Good bye!\n")
        return None, "q", None
    i = input("\n\tPlease type your {}: ".format(i_type))
    u = None
    if i_type.lower() == "user":
        u = ts.query.query_user_info(i)
    while i_type.lower() == "user" and u is None:
        print("\tSearch for Username Failed. Try a different Username.")
        i = input("\n\tPlease type your {}: ".format(i_type))
        u = ts.query.query_user_info(i)
    return i, i_type, u


def scrape_tweets(i, i_type):
    """
    This function takes the input from the user and performs a query for
    matching Tweets using the query function of the twitterscraper
    library. This query changes based on whether or not the user was
    selecting a keyword or user for the query. For the "user" category,
    the function asks for 500 tweets from a specific account. For the
    "keyword" category, the function asks for 500 tweets from the last
    2 weeks with that keyword.
    Arguments: i      -- The value inputted by the user
               i_type -- Indicator for if the input is a user or keyword
    Returns: The list of Tweet objects returned by the query
    """
    print("\n\tScraping Data from Twitter based on Certain Criteria...\n")
    if i_type.lower() == "user":
        print("\tScraping Tweet Data for User: {}...\n".format(i))
        r = ts.query.query_tweets_from_user(i, limit=500)
    if i_type.lower() == "keyword":
        print("\tScraping Tweet Data for Keyword: {}...\n".format(i))
        date = dt.date.today() - dt.timedelta(days=14)
        r = ts.query.query_tweets(i, limit=500, begindate=date, lang="en")
    return r


def format_data(i, data, u, i_type):
    """
    Takes the data returned by the tweet queries in the form of tweet objects
    and formats it to make further analysis of text in tweets easier. For the
    tweet texts, this function removes links and newlines in tweets.
    Arguments: i      -- user-inputted value
               data   -- List of tweet objects returned by the query
               u      -- A user object to check that tweets are from user
                         (not retweets)
               i_type -- The type of the user inputted value
    Returns: Both the filtered tweet list and the formatted tweet texts
    """
    print("\tFormatting Tweet Data for Text Analysis...\n")
    if i_type == 'user':
        data = list(filter(lambda a: u.user == a.screen_name, data))
    if i_type == 'keyword':
        data = list(filter(lambda a: i in a.text.lower(), data))
    tx = [re.sub(r'(pic.|http).*', '', t.text).replace('\n', '') for t in data]
    return data, list(filter(lambda a: len(a) > 3, tx))


def find_freq_words(text):
    """
    Takes the text data for the Tweets and first finds the top 10 most used
    alphabetical words. Then, the function does the same thing, but only
    including stop words. In NLP stop words are common words like 'of', 'and',
    and 'the' that don't communicate any information or sentiment and are
    therefore not helpful in training a model. Removing stop words reveals the
    words with more contextual meaning. These two top 10 lists are
    then printed out to the screen.
    Arguments: text -- A list of tweet text based on users query
    Returns: N/A
    """
    stop = n.corpus.stopwords.words('english')
    w = list(it.chain(*[word_tokenize(p) for p in text]))
    w = [x.lower() for x in list(filter(lambda a: a.isalpha(), w))]
    print("\tMost Common Words:")
    [print("\t {} ({})".format(k, v)) for k, v in c.Counter(w).most_common(10)]
    w = list(filter(lambda a: a not in stop, w))
    print("\n\tMost Common Relevant Words:")
    [print("\t {} ({})".format(k, v)) for k, v in c.Counter(w).most_common(10)]


def start_data_analysis(data, text, input, i_type):
    """
    Takes the data returned by the tweet queries in the form of tweet objects
    and formats it to make further analysis of text in tweets easier. For the
    tweet texts, this function removes links and newlines in tweets.
    Arguments: data   -- A list of tweet objects returned by the query
               text   -- A list of tweet texts pulled from data and formatted
               input  -- The value inputted by the user
               i_type -- The indicator for if the input is a user or keyword
    Returns: The results of basic data analysis in the form of a dict
    """
    results = {}
    if len(text) == 0:
        print("\t\tError: No Tweet Data for Selection\n")
        return None
    print("\tPerforming Data Analysis on Tweet Results...\n")
    if i_type.lower() == "user":
        u = ts.query.query_user_info(input)
        results['Username'] = u.user
        results['Name'] = u.full_name
        results['Followers'] = u.followers
        results['Following'] = u.following
    else:
        results['Keyword'] = input
    results['Total Recent Tweets Loaded'] = len(text)
    recent = max(data, key=lambda t: t.timestamp)
    liked = max(data, key=lambda t: t.likes)
    retweeted = max(data, key=lambda t: t.retweets)
    lens = [len(a) for a in text]
    likes = [a.likes for a in data]
    results['Average Tweet Length'] = round(sum(lens) / len(lens), 2)
    results['Average Likes'] = round(sum(likes) / len(likes), 2)
    results['Max Tweet Length'] = [max(text, key=len), len(max(text, key=len))]
    results['Min Tweet Length'] = [min(text, key=len), len(min(text, key=len))]
    results['Most Recent Tweet'] = [recent.text, str(recent.timestamp)]
    results['Most Liked Tweet'] = [liked.text, liked.likes]
    results['Most Retweeted Tweet'] = [retweeted.text, retweeted.retweets]
    return results


def main():
    """
    This is the main function of the program. It is responsible for carrying
    out the major processes of the program and calling the other functions
    defined above. The function starts by handling printouts and getting user
    input. It then, calls for Twitter queries based on that user input. Data
    is pulled from these query results and is printed to the screen. Next, a
    Naive-Bayes Classification model is used to perform basic Sentiment
    Analysis on 50 random Tweets from the query. This data is also printed to
    the screen. Then, the user has the option to re-query or quit.
    """
    # m.build_model() # Uncomment to retrain
    m.download_nltk_packages()
    disable_logger(True)
    welcome_printout()
    while True:
        i, i_type, u = get_user_input()
        if i_type == 'q':
            break
        if i_type == 'tweet':
            c = pickle.load(open("classifier1.pickle", "rb"))
            result = c.classify({x: True for x in m.clean(word_tokenize(i))})
            twt_print("\n\t\t({}) {}\n".format(result, i))
            continue
        data, text = format_data(i, scrape_tweets(i, i_type), u, i_type)
        results = start_data_analysis(data, text, i, i_type)
        if results is None:
            continue
        print("\t{}\n\tInitial Data Analysis:\n".format("----"*16))
        [twt_print("\t{}: {}\n".format(r, results[r])) for r in results]
        find_freq_words(text)
        m.perform_sentiment_analysis(text)


if __name__ == '__main__':
    main()
