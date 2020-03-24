"""
CS 41 Final Project: Tweet Sentiment Analysis
Authors: Ruben Sanchez and Erick Hernandez
SUNet: rubensan & erickha

This script will aggregate tweets under a certain hashtag, and take keywords under those tweets.
From there, it will do sentiment analysis on tweets that contain the keywords to see how they change
"""
import sys
import argparse
import yaml
from os import path
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import tweepy
import subprocess
import jsonpickle
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

def displayAnalysis(argDict, sentiments): 
    #uses matpot lib to graph the senitment
    print("Displaying analysis")
    n_groups = len(sentiments) - 2
    start = []
    end = []
    for keyword in argDict["keywords"]: 
        scores = sentiments[keyword]
        start.append(scores[0])
        end.append(scores[1])

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.75

    rects1 = plt.bar(index, start, bar_width,
    alpha=opacity,
    color='b',
    label="Start: " + sentiments["startDateTime"])

    rects2 = plt.bar(index + bar_width, end, bar_width,
    alpha=opacity,
    color='r',
    label="End: " + sentiments["endDateTime"])

    #plot labels
    plt.xlabel('Keywords')
    plt.ylabel('Sentiment Score')
    plt.title('Tweet Sentiment Analysis')
    plt.xticks(index + bar_width/2, argDict["keywords"])
    plt.legend()

    #displays graph
    plt.tight_layout()
    plt.show()


def analyzeTweets(argDict): 
    #using the textblob library, we can traverse parsed tweets and categorize them
    sentiments = {}
    fName = '.parsed-tweets.txt'
    tweets = []
    with open(fName, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tweets.append(tweet)
    tweets = list(reversed(tweets))
    half = len(tweets) / 2
    # loops over keywords
    for keyword in argDict["keywords"]:
        start = 0
        end = 0
        count = 0
        # loops over all tweets searching for keywords
        for t in tweets: 
            count += 1
            if keyword.lower() in t["content"].lower(): 
                score = TextBlob(t["content"])
                if (count < half): 
                    start += score.sentiment.polarity                  
                else: 
                    end += score.sentiment.polarity
        sentiments[keyword] = (start/half, end/half)
    sentiments["startDateTime"] = tweets[0]["timestamp"]
    sentiments["endDateTime"] = tweets[len(tweets) - 1]["timestamp"]
    return sentiments



def loadTweets(argDict):
    #auth tokens provided by twitter for developers
    auth = tweepy.OAuthHandler("1OY1cxVgUXZFoMgvxq1eEKpjx", "LukFltoFXodtADUHCjZ0IaN1C7ous7uo2ZgqQ01HLmTWatXgMw")
    auth.set_access_token("1147601573993803776-UmfCvlhkRxogSmDyIU6iF7k58yoD1c", "jmL3TMCfI6NPZrEoH0rMvtv2l7fRU3Ueyxj6Z8dFVNLQQ")

    api = tweepy.API(auth)

    searchQuery = '#' + argDict["hashtag"]  # this is what we're searching for
    maxTweets = 10000 # max number of tweets (Twitter only allows 18k tweets/15 min)
    tweetsPerQry = 100  # this is the max the API permits
    fName = '.tweets.txt' # We'll store the tweets in a text file.

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'w') as f:
        while tweetCount < maxTweets:
            try:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                            '\n')
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
    subprocess.call(["rm", ".cached.txt"])
    with open(".cached.txt", 'w') as file: 
        file.write(argDict["hashtag"])

def parseTweets():
    #goes through the downloaded tweets file to clean up tweets and extract relvant info (timestamp and content)
    fReadName = '.tweets.txt'
    fWriteName = '.parsed-tweets.txt'
    with open(fWriteName, 'w') as parsed:
        with open(fReadName, 'r') as f:
            for line in f:
                # creates json object, one per line that contains timestamp and contents
                tweetDict = {}
                tweet=jsonpickle.decode(line)
                tweetDict["timestamp"] = (tweet["created_at"])
                text = tweet["text"]
                index = text.find(':')
                text = text[index + 2:]
                tweetDict["content"] = text
                json.dump(tweetDict, parsed)
                parsed.write('\n')


def main(argv):
    #parser to parse the name of the config file we are passed
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file', help= "realtive path to yaml file with config")
    args = parser.parse_args()
    filename = args.file.strip()

    #opens the config file and loads the arguments into a dict
    with open(filename) as file: 
        argDict = yaml.full_load(file)
    
    #gets the name of the most recently cached tweets that fall under a hashtag
    cachedFile = '.cached.txt'
    cachedHastag = ''
    if (path.exists(cachedFile)):
        with open(cachedFile, 'r') as file: 
            for line in file:
                cachedHastag = line

    #does not load tweets if the hashtag has already been cached
    if (cachedHastag != argDict["hashtag"]):
        print("Tweets not cached. Will download now")
        loadTweets(argDict) # conditional on the fact that the tweets we might have already saved
        parseTweets()
    else:
        print ("Tweets for this hashtag have been cached. Fast-forwarding to rendering them")

    # parses and analyzes the tweets
    sentiments = analyzeTweets(argDict)
    displayAnalysis(argDict, sentiments)

if __name__ == "__main__":
    main(sys.argv)