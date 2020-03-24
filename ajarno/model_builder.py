# !/usr/bin/env python3
"""Final Project: TweetInsight - Twitter Analytics Tool (Model Builder Module)
Name: AJ Arnolie
Date: 3/10/20
SUNet: ajarno
----------------------------------------------------------------------------
This module provides sentiment analysis training and application capabilities
to the main function of the TweetInsight project. This file contains the
functions for training and saving the Naive-Bayes Classification Model as
well as for applying this model to perform sentiment analysis on the tweets 
that are pulled from the internet in the main program. The functions that
are defined in this file are called in the main file for the program.
----------------------------------------------------------------------------
"""

# Imports for Various Libraries used in Program
import pickle
import nltk as n
from nltk.tokenize import word_tokenize as tokenize
import string
import random

import tweet_insight as t


def download_nltk_packages():
    """
    Downloads relevant NLTK packages for tokenization and classification later
    in the program.
    Arguments: N/A
    Returns: N/A
    """
    n.download('punkt')
    n.download('wordnet')
    n.download('stopwords')
    n.download('averaged_perceptron_tagger')


def clean_training_data():
    """
    Loads in the training data and other necessary packages from nltk and then
    formats the training data so that it is fully prepared for the Naive-Bayes
    Classification model. Finally, each tweet is formatted as a list with a
    dictionary entry for each word and a tag for '+' or '-' depending on the
    category of the tweet. These lists of cleaned sentences are combined,
    shuffled, and returned.
    Arguments: N/A
    Returns: Formatted data prepared for Naive-Bayes model training
    """
    n.download('twitter_samples')
    pos = n.corpus.twitter_samples.tokenized('positive_tweets.json')
    neg = n.corpus.twitter_samples.tokenized('negative_tweets.json')
    pos = [clean(p) for p in pos]
    neg = [clean(n) for n in neg]
    pos = [({x: True for x in p}, "+") for p in pos]
    neg = [({y: True for y in n}, "-") for n in neg]
    added = pos + neg
    random.shuffle(added)
    return added


def clean(ws):
    """
    This function takes the tokenized tweets and formats them to prepare
    for model training. This involves removing stopwords, tokenizing and
    lemmatizing each word in each tweet, removing punctuation and invalid
    lines, and returning all words in lowercase.
    Arguments: set  -- A list of tokenized word for a single tweet
    Returns: The formatted list of words in lowercase
    """
    punct = string.punctuation
    stop = n.corpus.stopwords.words('english')
    ws = list(filter(lambda a: a[0] != "@" and "http" not in a, ws))
    t = n.tag.pos_tag(ws)
    tag = [w[1][0] if w[1][:1] == 'NN' or w[1][:1] == 'VB' else 'a' for w in t]
    lem = n.stem.wordnet.WordNetLemmatizer()
    ws = [lem.lemmatize(a, b.lower()) for a, b in zip(ws, tag)]
    ws = list(filter(lambda a: len(a) > 0 and a not in punct, ws))
    ws = list(filter(lambda a: a.lower() not in stop, ws))
    return [p.lower() for p in ws]


def save_classifier_model(classifier):
    """
    This function allows the classifier to be saved using pickle after
    training. This way, each time the program is run after training, the
    model doesn't have to be retrained, and we can instead simply load it
    from the pickle file.
    Arguments: classifier -- The classifier returned by NLTK to be saved
    Returns: N/A
    """
    with open('classifier1.pickle', 'wb') as f:
        pickle.dump(classifier, f, protocol=pickle.HIGHEST_PROTOCOL)


def build_model():
    """
    This function builds the Naive-Bayes Classification model using the
    loaded data, saves this classifier as a pickle file, and then exits
    the program. Because this function only needs to be run once, it is
    commented out in the main function. In order to retrain the classifier,
    just uncomment this function in main.
    Arguments: N/A
    Returns: N/A
    """
    download_nltk_packages()
    data = clean_training_data()
    classifier = n.NaiveBayesClassifier.train(data[:9000])
    correct = n.classify.accuracy(classifier, data[9000:])
    print("\nModel is {}% correct for testing data.\n".format(correct*100))
    save_classifier_model(classifier)
    quit()


def determine_sentiment(pos_cnt, neg_cnt):
    """
    Determines the sentiment based on what percentage of the classified
    tweets were determined to have positive sentiment.
    Arguments: N/A
    Returns: A string associated with sentiment of the set of Tweets
    """
    pos_pct = (pos_cnt * 100) / (pos_cnt + neg_cnt)
    sent = ""
    if pos_pct > 85:
        sent = "Very Positive"
    elif pos_pct > 70:
        sent = "Positive"
    elif pos_pct > 55:
        sent = "Mildly Positive"
    elif pos_pct > 45:
        sent = "Neutral"
    elif pos_pct > 30:
        sent = "Mildly Negative"
    elif pos_pct > 15:
        sent = "Negative"
    else:
        sent = "Very Negative"
    return sent


def perform_sentiment_analysis(txt):
    """
    This function is responsible for the sentiment analysis portion of the
    program. It first loads the saved and trained classification model into
    the program to be used. The function then uses the trained Naive-Bayes
    Classifier model to do Sentiment Analysis on 50 randomly selected Tweets
    out of the Tweets from the user's query in order to analyze the tone of
    these Tweets and make a prediction as to whether it is positive or
    negative. Each result is printed along with its related string to the.
    screen. Finally, the overall sentiment is determined by calculation the
    percent positive sentiment results over the 50 randomly selected Tweets.
    Arguments: text -- The tweet texts used for sentiment analysis by the model
    Returns: N/A
    """
    print("\n\t{}".format("----"*16))
    print("\tSentiment Analysis:\n")
    c = pickle.load(open("classifier1.pickle", "rb"))
    print("\tUsing Naive-Bayes Classification Model to Analyze Tweets: \n")
    random.shuffle(txt)
    cl = [c.classify({x: True for x in clean(tokenize(p))}) for p in txt[:50]]
    [t.twt_print("\t({}) {}".format(a, p)) for a, p in zip(cl[:50], txt[:50])]
    pos_cnt = cl.count("+")
    neg_cnt = cl.count("-")
    sent = determine_sentiment(pos_cnt, neg_cnt)
    print("\n\tOverall Sentiment: {} ({}/{} +)".format(sent, pos_cnt, len(cl)))
    print("\n\t{}\n".format("----"*16))
